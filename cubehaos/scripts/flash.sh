#!/usr/bin/env bash
# High-consequence operation. Never run this unless you are physically
# connected to Cube UMS and have a verified, tested image.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[[ $# -eq 2 ]] || { echo 'Usage: flash.sh haos_cube2v0eu-VERSION.img.xz /dev/sdX' >&2; exit 2; }
IMAGE="$(realpath "$1")"; DEST="$(realpath "$2")"
[[ -f "$IMAGE" && "$IMAGE" == *haos_cube2v0eu-*.img.xz ]] || { echo 'Cube installation image required' >&2; exit 2; }
[[ -b "$DEST" ]] || { echo 'Destination must be an existing block device' >&2; exit 2; }
[[ $(id -u) -eq 0 ]] || { echo 'Must run as root on host PC' >&2; exit 1; }
for tool in lsblk xz dd sync python3; do command -v "$tool" >/dev/null || { echo "Missing $tool" >&2; exit 1; }; done
[[ "$(lsblk -dn -o TYPE "$DEST" | xargs)" == disk ]] || { echo 'Only a whole disk, not a partition' >&2; exit 1; }
[[ "$(lsblk -dn -o TRAN "$DEST" | xargs)" == usb ]] || { echo 'Refusing any non-USB disk' >&2; exit 1; }
SIZE="$(lsblk -bdno SIZE "$DEST" | xargs)"
[[ "$SIZE" =~ ^[0-9]+$ ]] || exit 1
# This stage targets the stock 8GB eMMC Cube. Larger upgraded modules need a
# separately tested installer; never silently widen the erase target.
((SIZE >= 7000000000 && SIZE <= 9000000000)) || { echo 'USB disk does not match expected Cube eMMC size' >&2; exit 1; }
if lsblk -nr -o MOUNTPOINTS "$DEST" | grep -q '[^[:space:]]'; then
  echo 'Target (or one of its partitions) is mounted. Refusing.' >&2; exit 1
fi
JSON="$(mktemp)"
trap 'rm -f "$JSON"' EXIT
python3 "$ROOT/scripts/inspect_image.py" "$(dirname "$IMAGE")" --json-out "$JSON" >/dev/null
read -r RAW_SIZE RAW_SHA < <(python3 - "$JSON" "$IMAGE" <<'PY'
import json,sys
from pathlib import Path
j=json.load(open(sys.argv[1]))
i=j['image']
if Path(sys.argv[2]).name!=i['file']: raise SystemExit('Image mismatch')
print(i['raw_bytes'],i['sha256_raw'])
PY
)
((RAW_SIZE < SIZE)) || { echo 'Image is bigger than eMMC media' >&2; exit 1; }
# No attempt to preserve original Futurehome software: full erase is intended.
# This is a deliberate physical installation, never automatic CI behavior.
echo 'Physical target to erase:'
lsblk -o NAME,PATH,SIZE,MODEL,SERIAL,TRAN,TYPE,MOUNTPOINTS "$DEST"
printf '\nRaw image bytes: %s\nVerification hash: %s\n' "$RAW_SIZE" "$RAW_SHA"
printf 'Type exactly ERASE-%s-%s to confirm: ' "$(basename "$DEST")" "$SIZE"
read -r CONFIRM
[[ "$CONFIRM" == "ERASE-$(basename "$DEST")-$SIZE" ]] || { echo 'Aborted'; exit 1; }
# Preflight is already full-stream; xz -t repeats integrity check before erasing.
xz -t "$IMAGE"
xz -dc "$IMAGE" | dd of="$DEST" bs=4M conv=fsync status=progress
sync
# Verify each byte of written image against the uncompressed image SHA256.
# This verifies the write, not device bootability or long-term eMMC health.
python3 - "$DEST" "$RAW_SIZE" "$RAW_SHA" <<'PY'
import hashlib,sys
path=sys.argv[1]; to_read=int(sys.argv[2]); expected=sys.argv[3]
h=hashlib.sha256()
with open(path,'rb', buffering=0) as f:
    while to_read:
        block=f.read(min(to_read,4*1024*1024))
        if not block: raise SystemExit('Readback failed: unexpected end')
        h.update(block); to_read-=len(block)
if h.hexdigest()!=expected: raise SystemExit('Readback SHA256 mismatch! Do not deploy this device.')
print('Full readback SHA256 matches. Physical boot and functional tests STILL REQUIRED.')
PY
