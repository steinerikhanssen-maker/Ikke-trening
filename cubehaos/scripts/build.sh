#!/usr/bin/env bash
# Fail closed: successful compilation must yield a completely scanned Cube image.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="${1:-$ROOT/work}"
cd "$WORK/operating-system"
[[ -f buildroot-external/configs/cube2v0eu_defconfig ]] || { echo 'Run bootstrap.sh first' >&2; exit 1; }
command -v docker >/dev/null || { echo 'A Linux builder with Docker is required' >&2; exit 1; }
mkdir -p output/images
# Deliberately reject old outputs: mix-and-match of HAOS versions could flash
# a mismatched bootloader/DTB/RAUC bundle.
if compgen -G 'output/images/haos_cube2v0eu-*' >/dev/null; then
  echo 'Previous Cube artifacts found. Use a fresh output dir/build container.' >&2
  exit 1
fi
python3 "$ROOT/scripts/static_preflight.py" "$WORK/operating-system"
scripts/enter.sh make cube2v0eu
python3 "$ROOT/scripts/inspect_image.py" "$WORK/operating-system/output/images" \
  --json-out "$WORK/operating-system/output/images/cube-release-inspection.json"
printf '\nBUILD ARTIFACTS VALIDATED STRUCTURALLY. NOT HARDWARE TESTED.\n'
