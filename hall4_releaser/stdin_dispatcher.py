"""Home Assistant Supervisor stdin bridge. No listening socket or scheduler.

Only Supervisor-authenticated hassio.app_stdin messages reach this process.
No remote URLs, free-form paths, shell commands or updates without a pinned
manifest. The actual file transaction runs OUTSIDE Home Assistant Core.
"""
from __future__ import annotations
import json
from pathlib import Path
import re
import subprocess
import sys
from threading import Lock, Thread
import time

CONFIG = Path("/config")
AGENT = Path("/app/hall4_update_agent.py")
RELEASES = CONFIG / "husvarme-release-staging" / "releases"
ID = re.compile(r"^hall4-[a-zA-Z0-9][a-zA-Z0-9_-]{2,63}$")
SHA = re.compile(r"^[0-9a-f]{64}$")
ACTIONS = frozenset(("preflight", "deploy", "rollback"))
ACTIVE = frozenset(("before_verified", "core_stopped", "new_files_verified", "automatic_rollback"))
STATE = {"active": None}
MUTEX = Lock()


def log(event, **data):
    print(json.dumps({"event": event, "at": time.time(), **data},
                     ensure_ascii=False, sort_keys=True), flush=True)


def json_stream(source, *, max_chars=4096):
    """Decode consecutive Supervisor JSON bodies even without newline separators."""
    decoder = json.JSONDecoder()
    buffer = ""
    while (char := source.read(1)) != "":
        if not buffer and char.isspace():
            continue
        buffer += char
        if len(buffer) > max_chars:
            log("input_refused", reason="max_length")
            buffer = ""
            continue
        try:
            value, end = decoder.raw_decode(buffer)
        except json.JSONDecodeError:
            continue
        if buffer[end:].strip():
            log("input_refused", reason="trailing_data")
        else:
            yield value
        buffer = ""


def validate(value):
    # Some older Supervisor actions send JSON-encoded strings.
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (ValueError, TypeError):
            raise ValueError("string_not_json_object") from None
    if type(value) is not dict or set(value) != {"command", "release_id", "manifest_sha256"}:
        raise ValueError("invalid_command_shape")
    if value["command"] not in ACTIONS:
        raise ValueError("unknown_command")
    if type(value["release_id"]) is not str or not ID.fullmatch(value["release_id"]):
        raise ValueError("bad_release_id")
    if type(value["manifest_sha256"]) is not str or not SHA.fullmatch(value["manifest_sha256"]):
        raise ValueError("bad_manifest_sha256")
    return value


def run(command):
    release_id = command["release_id"]
    action = command["command"]
    argv = [sys.executable, "-I", "-B", str(AGENT), action,
            "--release-id", release_id,
            "--manifest-sha256", command["manifest_sha256"],
            "--config-dir", str(CONFIG)]
    try:
        result = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, check=False)
        log("operation_result", release_id=release_id, action=action,
            returncode=result.returncode, output=result.stdout[-1200:])
        return result.returncode == 0
    except Exception as e:
        log("operation_failed", release_id=release_id, action=action,
            error_type=type(e).__name__)
        return False
    finally:
        with MUTEX:
            STATE["active"] = None


def enqueue(raw):
    try:
        command = validate(raw)
    except ValueError as e:
        log("input_refused", reason=str(e))
        return False
    with MUTEX:
        if STATE["active"] is not None:
            log("busy_no_parallel_release", requested=command["release_id"])
            return False
        STATE["active"] = command["release_id"]
    Thread(target=run, args=(command,), name="hall4-release", daemon=True).start()
    log("accepted", release_id=command["release_id"], action=command["command"])
    return True


def recover_previous():
    """Recover an interrupted approved transaction after app process restart."""
    if not RELEASES.is_dir() or RELEASES.is_symlink():
        return
    candidates = []
    for folder in RELEASES.iterdir():
        if folder.is_symlink() or not folder.is_dir() or not ID.fullmatch(folder.name):
            continue
        state_file = folder / "state.json"
        if not state_file.is_file() or state_file.is_symlink():
            continue
        try:
            obj = json.loads(state_file.read_text())
        except (ValueError, OSError):
            log("recovery_unreadable", release_id=folder.name)
            raise RuntimeError("Unverifiable transaction state; refusing all new releases") from None
        if type(obj) is not dict:
            raise RuntimeError("Invalid transaction state; refusing all new releases")
        if obj.get("phase") in ("FAILED_RECOVERY_REQUIRED", "ROLLBACK_NOT_VERIFIED"):
            raise RuntimeError("Previous recovery failed; refusing all new releases")
        if obj.get("phase") not in ACTIVE:
            continue
        if (obj.get("release_id") != folder.name
                or type(obj.get("manifest_sha256")) is not str
                or not SHA.fullmatch(obj["manifest_sha256"])):
            log("recovery_untrusted_state", release_id=folder.name)
            raise RuntimeError("Interrupted release cannot be authenticated")
        candidates.append((folder.name, obj["manifest_sha256"]))
    if not candidates:
        return
    if len(candidates) != 1:
        log("recovery_ambiguous_multiple_transactions", count=len(candidates))
        raise RuntimeError("Manual recovery necessary; multiple interrupted releases")
    release_id, pin = candidates[0]
    log("interrupted_release_recovery", release_id=release_id)
    cmd = {"command": "rollback", "release_id": release_id, "manifest_sha256": pin}
    if not run(cmd):
        raise RuntimeError("Interrupted Hall4 release could not be recovered; refusing new releases")


def main():
    log("started", stdin_only=True, config=str(CONFIG))
    recover_previous()
    for value in json_stream(sys.stdin):
        enqueue(value)
    log("stdin_closed")


if __name__ == "__main__":
    main()
