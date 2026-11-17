#!/usr/bin/env bash
# Run the Rockchip UMS loader from RAM. Never writes Cube eMMC directly.
# UMS makes eMMC writable to the host OS: do not mount it or auto-format it.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOADER="${1:-${CUBE_WORK:-$ROOT/work}/board-support/cube2v0eu-maskrom-uboot-ums.bin}"
[[ -s "$LOADER" ]] || { echo 'Missing RAM loader; run build_ram_loader.sh' >&2; exit 1; }
for x in rkdeveloptool lsblk; do command -v "$x" >/dev/null || { echo "Missing $x" >&2; exit 1; }; done
probe(){ rkdeveloptool ld; }
BEFORE="$(probe)"
count="$(grep -Ec 'Maskrom|Loader' <<< "$BEFORE" || true)"
[[ "$count" -eq 1 ]] || { printf 'Expected exactly one Rockchip USB device; got:\n%s\n' "$BEFORE" >&2; exit 1; }
printf 'Before attaching Cube UMS, host disks:\n'
lsblk -o NAME,PATH,SIZE,MODEL,SERIAL,TRAN,TYPE,MOUNTPOINTS
printf '\nRockchip USB:\n%s\n' "$BEFORE"
read -r -p 'Type RAM to launch RAM-only loader: ' ANSWER
[[ "$ANSWER" == RAM ]] || exit 1
if grep -q Loader <<< "$BEFORE"; then
  rkdeveloptool rd 3
  for _ in {1..12}; do
    sleep 1
    [[ "$(probe)" == *Maskrom* ]] && break
  done
fi
AFTER="$(probe)"
[[ "$AFTER" == *Maskrom* ]] || { echo 'Rockchip is not in Maskrom; refusing RAM loader' >&2; exit 1; }
rkdeveloptool db "$LOADER"
printf '\nAfter UMS launch:\n'
sleep 3
lsblk -o NAME,PATH,SIZE,MODEL,SERIAL,TRAN,TYPE,MOUNTPOINTS
printf '\nIdentify the new USB-attached ~8 GB disk; no write was performed.\n'
