"""Bounded, owner-triggered Hall4 component release agent.

Run in an already-authorized Supervisor app, NOT inside Home Assistant Core.
No network downloads, shell inputs, schedules or generic filesystem writes.
"""
from __future__ import annotations
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ALLOWED = frozenset({"__init__.py", "sensor.py", "model.py", "control.py", "mixing.py",
    "ha.py", "energy.py", "observer.py", "evidence.py", "driver.json", "manifest.json",
    "thermal_seed.json"})
ALLOWED_RELEASE = re.compile(r"^hall4-[a-zA-Z0-9][a-zA-Z0-9_-]{2,63}$")
PINNED_DEPENDENCIES = frozenset({"__init__.py", "driver.json", "evidence.py"})
MAX_FILE_BYTES = 262144


class Refused(RuntimeError):
    pass


def require(ok, why):
    if not ok:
        raise Refused(why)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git_blob_sha(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode("ascii") + b"\x00" + b).hexdigest()


def canonical_json(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def read_regular(p: Path, cap=MAX_FILE_BYTES):
    require(not p.is_symlink() and p.is_file(), f"missing_or_symlink:{p.name}")
    require(p.stat().st_size <= cap, f"file_too_large:{p.name}")
    return p.read_bytes()


def safe_write(p: Path, data: bytes, mode: int, owner=None):
    require(not p.is_symlink(), f"symlink_target:{p.name}")
    require(p.parent.is_dir() and not p.parent.is_symlink(), "missing_target_folder")
    with tempfile.NamedTemporaryFile(dir=p.parent, delete=False) as f:
        tmp = Path(f.name)
        try:
            f.write(data)
            f.flush()
            if owner is not None:
                os.fchown(f.fileno(), *owner)
            os.fchmod(f.fileno(), mode)
            os.fsync(f.fileno())
            os.replace(tmp, p)
            fd = os.open(p.parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
        finally:
            tmp.unlink(missing_ok=True)


def load_manifest(release: Path, expected_sha: str):
    require(re.fullmatch(r"[0-9a-f]{64}", expected_sha) is not None, "invalid_pin")
    raw = read_regular(release / "manifest.json", 32768)
    require(sha(raw) == expected_sha, "manifest_sha_mismatch")
    obj = json.loads(raw)
    require(obj.get("schema") == 1, "unknown_schema")
    require(ALLOWED_RELEASE.fullmatch(obj.get("release_id", "")) is not None, "invalid_release_id")
    require(re.fullmatch(r"[0-9a-f]{40}", obj.get("source_commit", "")) is not None,
            "invalid_commit_id")
    require((release / "after").is_dir() and not (release / "after").is_symlink(),
            "symlink_or_missing_after_directory")
    files = obj.get("files")
    require(type(files) is dict and 1 <= len(files) <= len(ALLOWED), "invalid_file_count")
    require(set(files) <= ALLOWED, "invalid_target_path")
    deps = obj.get("dependencies")
    require(type(deps) is dict and set(deps) == PINNED_DEPENDENCIES, "invalid_dependencies")
    for name, h in deps.items():
        require(re.fullmatch(r"[0-9a-f]{64}", h or "") is not None, "bad_dependency_sha")
    for name, spec in files.items():
        require(type(spec) is dict and set(spec) == {"before_sha256", "after_sha256", "after_blob_sha1"},
                "invalid_file_spec")
        for key, size in (("before_sha256", 64), ("after_sha256", 64), ("after_blob_sha1", 40)):
            value = spec[key]
            require(value is None and key == "before_sha256" or
                    type(value) is str and re.fullmatch(r"[0-9a-f]{%d}" % size, value) is not None,
                    f"bad_hash:{name}:{key}")
        after = read_regular(release / "after" / name)
        require(sha(after) == spec["after_sha256"] and git_blob_sha(after) == spec["after_blob_sha1"],
                f"payload_mismatch:{name}")
    return obj


class Core:
    """Use the documented authenticated Supervisor endpoints from a separate app."""
    def __init__(self, timeout=420):
        self.timeout = timeout

    def _request(self, url, data=None, timeout=12, *, supervisor_envelope=True):
        token = os.environ.get("SUPERVISOR_TOKEN")
        require(token is not None and bool(token), "missing_supervisor_token")
        req = Request("http://supervisor" + url, data=data,
                      headers={"Authorization": "Bearer " + token,
                               "Content-Type": "application/json"})
        try:
            with urlopen(req, timeout=timeout) as response:
                value = json.load(response)
        except HTTPError as err:
            # In recovery, do not make "already stopped" itself an obstacle.
            message = err.read(4096).decode("utf-8", "replace").lower()
            action = url.rsplit("/", 1)[-1]
            if (action == "stop" and any(x in message for x in ("already stopped", "not running"))
                    or action == "start" and "already running" in message):
                return {"result": "ok"}
            raise Refused(f"supervisor_{action}_http_{err.code}") from err
        except URLError as err:
            raise Refused("supervisor_not_reachable") from err
        require(isinstance(value, dict), "supervisor_invalid_response")
        if supervisor_envelope:
            require(value.get("result") == "ok", "supervisor_request_refused")
        return value

    def command(self, action):
        require(action in ("check", "stop", "start"), "invalid_lifecycle_action")
        self._request("/core/" + action, data=b"{}", timeout=self.timeout)

    def healthy(self):
        state = self._request("/core/api/states/sensor.hall4_plan", supervisor_envelope=False)
        attrs = state.get("attributes") or {}
        plan = attrs.get("plan") or {}
        require(state.get("state") == "normal", "hall4_owner_not_normal")
        tick = plan.get("at")
        require(type(tick) in (float, int) and abs(time.time() - tick) <= 95,
                "hall4_plan_not_fresh")
        require(isinstance(plan.get("ir"), list) and isinstance(plan.get("fan"), list),
                "hall4_plan_missing_channels")
        return attrs


class Agent:
    def __init__(self, config: Path, release_id: str, manifest_pin: str, core=None):
        require(ALLOWED_RELEASE.fullmatch(release_id) is not None, "bad_release_id")
        self.config = config.resolve(strict=True)
        stage = self.config / "husvarme-release-staging"
        releases = stage / "releases"
        require(stage.is_dir() and releases.is_dir() and not stage.is_symlink()
                and not releases.is_symlink(), "unsafe_staging_folder")
        self.release = releases / release_id
        self.live = self.config / "custom_components" / "hall4"
        require(self.live.is_dir() and not self.live.is_symlink(), "no_hall4_folder")
        require(self.release.is_dir() and not self.release.is_symlink(), "release_not_staged")
        self.manifest = load_manifest(self.release, manifest_pin)
        require(self.manifest["release_id"] == release_id, "wrong_release_folder")
        self.pin = manifest_pin
        self.core = core or Core()
        self.before = self.release / "before"
        self.state = self.release / "state.json"

    def lock(self):
        fd = os.open(self.config / "husvarme-release-staging" / "hall4-release.lock",
                     os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return fd

    def current(self):
        data = {}
        for name, spec in self.manifest["files"].items():
            p = self.live / name
            data[name] = sha(read_regular(p)) if p.exists() else None
            require(data[name] in (spec["before_sha256"], spec["after_sha256"]),
                    f"unexpected_active_hash:{name}")
        for name, expected in self.manifest["dependencies"].items():
            require(sha(read_regular(self.live / name)) == expected, f"changed_dependency:{name}")
        return data

    def phase(self, name, **kw):
        body = {"phase": name, "release_id": self.manifest["release_id"],
                "source_commit": self.manifest["source_commit"],
                "manifest_sha256": self.pin, "at": time.time(), **kw}
        safe_write(self.state, canonical_json(body), 0o600)

    def backup(self):
        if self.before.exists():
            require(self.before.is_dir() and not self.before.is_symlink(), "bad_backup_directory")
        else:
            self.before.mkdir(mode=0o700)
        for name, spec in self.manifest["files"].items():
            path = self.before / name
            if spec["before_sha256"] is None:
                require(not path.exists(), "unexpected_backup_new_file")
                continue
            if not path.exists():
                data = read_regular(self.live / name)
                require(sha(data) == spec["before_sha256"], "backup_source_changed")
                safe_write(path, data, stat.S_IMODE((self.live / name).stat().st_mode))
            require(sha(read_regular(path)) == spec["before_sha256"], "backup_hash_mismatch")

    def install_files(self, to_after):
        for name, spec in self.manifest["files"].items():
            p = self.live / name
            source = self.release / "after" / name if to_after else self.before / name
            target = spec["after_sha256"] if to_after else spec["before_sha256"]
            if target is None:
                require(not p.is_symlink(), "symlink_target")
                if p.exists():
                    p.unlink()
                continue
            data = read_regular(source)
            require(sha(data) == target, "staged_or_backup_hash_mismatch")
            existing = p if p.exists() else self.live / "control.py"
            st = existing.stat()
            mode = stat.S_IMODE(st.st_mode) if p.exists() else 0o644
            if not p.exists() or sha(read_regular(p)) != target:
                safe_write(p, data, mode, (st.st_uid, st.st_gid))
        self.assert_state(to_after)

    def assert_state(self, after):
        for name, spec in self.manifest["files"].items():
            p = self.live / name
            expected = spec["after_sha256"] if after else spec["before_sha256"]
            current = sha(read_regular(p)) if p.exists() else None
            require(current == expected, f"post_hash_mismatch:{name}")

    def deploy(self, check_only=False):
        fd = self.lock()
        stopped = changed = False
        try:
            hashes = self.current()
            old = {n: spec["before_sha256"] for n, spec in self.manifest["files"].items()}
            new = {n: spec["after_sha256"] for n, spec in self.manifest["files"].items()}
            require(hashes == old or hashes == new, "mixed_version_do_not_guess")
            if hashes == new:
                attrs = self.core.healthy()
                require("forecast" in attrs and "metered_pairs" in attrs,
                        "new_code_not_loaded")
                self.phase("already_installed")
                return "already_installed"
            self.core.healthy()
            self.core.command("check")
            if check_only:
                self.phase("preflight_passed")
                return "preflight_passed"
            self.backup()
            self.phase("before_verified")
            self.core.command("stop")
            stopped = True
            self.phase("core_stopped")
            changed = True
            self.install_files(True)
            self.core.command("check")
            self.phase("new_files_verified")
            self.core.command("start")
            stopped = False
            # The natural coordinator updates once/minute. The caller can use status/verify
            # later; do not claim success until the Core service exposes fresh live state.
            for _ in range(36):
                time.sleep(5)
                try:
                    attrs = self.core.healthy()
                    require("forecast" in attrs and "metered_pairs" in attrs,
                            "new_version_not_loaded")
                    self.assert_state(True)
                    self.phase("installed_verified")
                    return "installed_verified"
                except (Refused, OSError, ValueError, TypeError, TimeoutError):
                    pass
            raise Refused("post_start_verification_failed")
        except Exception as err:
            if changed:
                self.phase("automatic_rollback", reason=type(err).__name__)
                try:
                    if not stopped:
                        self.core.command("stop")
                    self.install_files(False)
                    self.core.command("check")
                    self.core.command("start")
                    self.phase("rolled_back")
                except Exception as rollback_err:
                    try:
                        self.core.command("start")
                    except Exception:
                        pass
                    self.phase("FAILED_RECOVERY_REQUIRED", reason=type(rollback_err).__name__)
                    raise Refused("ROLLBACK_FAILED_MANUAL_RECOVERY_REQUIRED") from rollback_err
            elif stopped:
                self.core.command("start")
            raise
        finally:
            os.close(fd)

    def rollback(self):
        fd = self.lock()
        stopped = False
        try:
            self.current()
            self.backup()
            self.core.command("stop")
            stopped = True
            self.install_files(False)
            self.core.command("check")
            self.core.command("start")
            stopped = False
            for _ in range(36):
                time.sleep(5)
                try:
                    attrs = self.core.healthy()
                    require("forecast" not in attrs, "old_component_not_loaded")
                    self.assert_state(False)
                    self.phase("rolled_back")
                    return "rolled_back"
                except (Refused, OSError, ValueError, TypeError, TimeoutError):
                    pass
            self.phase("ROLLBACK_NOT_VERIFIED")
            raise Refused("rollback_not_verified")
        finally:
            if stopped:
                try:
                    self.core.command("start")
                except Exception:
                    self.phase("FAILED_RECOVERY_REQUIRED")
            os.close(fd)


def main():
    p = argparse.ArgumentParser(description="Local Hall4 release agent; invoke only from authorized Supervisor app")
    p.add_argument("command", choices=("preflight", "deploy", "rollback"))
    p.add_argument("--release-id", required=True)
    p.add_argument("--manifest-sha256", required=True)
    p.add_argument("--config-dir", type=Path, default=Path("/config"))
    a = p.parse_args()
    agent = Agent(a.config_dir, a.release_id, a.manifest_sha256)
    print(agent.rollback() if a.command == "rollback" else agent.deploy(check_only=a.command == "preflight"))


if __name__ == "__main__":
    main()
