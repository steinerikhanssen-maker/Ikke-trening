#!/usr/bin/env bash
# Read-only discovery. Does not reset, flash or change the Cube.
set -euo pipefail
if ! command -v rkdeveloptool >/dev/null 2>&1; then
  echo 'Installer/bygg rkdeveloptool på Linux-PC-en først.' >&2
  exit 1
fi
printf 'Rockchip USB devices (read-only):\n'
rkdeveloptool ld
printf '\nHvis listen er tom: bruk USB-C datakabel, hold funksjonsknappen\n'
printf 'mens Cube får strøm, og prøv igjen.\n'
