#!/usr/bin/env python3
"""Rebuild original GymNotFound Codex animation handoff from GitHub binary parts.

No third-party Python dependencies.
"""
from pathlib import Path
import hashlib
import os
import sys
import zipfile

HERE = Path(__file__).resolve().parent
NAME = "GymNotFound_Codex_Profesjonell_Animasjon.zip"
PART_COUNT = 14
EXPECTED_SIZE = 7864379
EXPECTED_SHA256 = "cdf2332a59d40e7ade8d5db839dba1f1d544ae3685449dd9f0cb5b0873283a6e"


def main():
    output = HERE / NAME
    temp = HERE / (NAME + ".tmp")
    digest = hashlib.sha256()
    total = 0
    try:
        with temp.open("wb") as target:
            for i in range(1, PART_COUNT + 1):
                source = HERE / f"{NAME}.part{i:02d}"
                if not source.is_file():
                    raise FileNotFoundError(f"Missing archive part: {source.name}")
                with source.open("rb") as fh:
                    while data := fh.read(1024 * 1024):
                        target.write(data)
                        digest.update(data)
                        total += len(data)
        if total != EXPECTED_SIZE:
            raise ValueError(f"Wrong size: {total} != {EXPECTED_SIZE}")
        if digest.hexdigest() != EXPECTED_SHA256:
            raise ValueError(f"SHA-256 mismatch: {digest.hexdigest()}")
        with zipfile.ZipFile(temp) as package:
            corrupt = package.testzip()
            if corrupt is not None:
                raise ValueError(f"Corrupt ZIP entry: {corrupt}")
            print(f"Verified {len(package.infolist())} ZIP entries")
        os.replace(temp, output)
    except Exception:
        temp.unlink(missing_ok=True)
        raise
    print(f"OK: {output}")
    print(f"SHA-256: {digest.hexdigest()}")
    print("Extract this archive and follow START_HER_CODEX.txt")


if __name__ == "__main__":
    sys.exit(main())
