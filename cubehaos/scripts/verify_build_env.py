#!/usr/bin/env python3
"""Read-only capability report. Never infers a bootable firmware from source tests."""
import json
import os
import shutil
import sys
from pathlib import Path

root=Path(__file__).resolve().parents[1]
checks={k:shutil.which(k) is not None for k in ("git","python3","docker","make","bash","rkdeveloptool","aarch64-linux-gnu-gcc")}
result={
    "project":"CubeHAOS-port-v0.3",
    "source_package_available":(root/"scripts/prepare_port.py").is_file(),
    "builder_has_internet": "not_tested_by_this_script",
    "host_tools":checks,
    "fully_buildable_here":all(checks[k] for k in ("git","python3","docker","make","bash")),
    "cube_connected":False,
    "bootable_image_verified":False,
    "approved_to_flash":False,
    "note":"Source package is NOT firmware. To approve an image requires a successful Buildroot build and physical Cube boot test."
}
print(json.dumps(result,indent=2,ensure_ascii=False))
