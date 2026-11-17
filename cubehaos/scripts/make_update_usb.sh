#!/usr/bin/env bash
# Offline upgrade packaging. Requires a real CONFIG-mounted filesystem.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[[ $# -eq 3 ]] || { echo 'Usage: make_update_usb.sh BUNDLE.raucb MOUNTED-CONFIG-ROOT TRUSTED-KEYRING.pem' >&2; exit 2; }
BUNDLE="$1"; USB="$2"; KEY="$3"
"$ROOT/scripts/verify_update.sh" "$BUNDLE" "$KEY" >/dev/null
command -v findmnt >/dev/null || { echo 'findmnt missing' >&2; exit 1; }
command -v lsblk >/dev/null || { echo 'lsblk missing' >&2; exit 1; }
mountpoint -q "$USB" || { echo 'Destination must be a filesystem mountpoint, not an ordinary folder' >&2; exit 1; }
SRC="$(findmnt -n -o SOURCE --target "$USB")"
FSTYPE="$(findmnt -n -o FSTYPE --target "$USB")"
LABEL="$(lsblk -n -o LABEL "$SRC" 2>/dev/null | head -1 | xargs || true)"
[[ "$LABEL" == CONFIG ]] || { echo "Expected mounted CONFIG label; found '$LABEL'" >&2; exit 1; }
[[ "$FSTYPE" == vfat || "$FSTYPE" == ext4 ]] || { echo 'CONFIG must use vfat or ext4' >&2; exit 1; }
cp -v -- "$BUNDLE" "$USB/"
sync
cmp -s "$BUNDLE" "$USB/$(basename "$BUNDLE")" || { echo 'Copy verification failed' >&2; exit 1; }
printf 'CONFIG media ready; connect to running HAOS, wait 5 minutes after startup, run: ha os import\n'
printf 'Import can also overwrite network and SSH-key settings based on CONFIG contents.\n'
