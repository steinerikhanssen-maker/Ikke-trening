#!/usr/bin/env bash
# Compiles a temporary U-Boot UMS loader; does not touch the Cube itself.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOARD="${CUBE_WORK:-$ROOT/work}/board-support"
[[ -d "$BOARD" ]] || { echo 'Kjør bootstrap.sh først' >&2; exit 1; }
for x in make wget git aarch64-linux-gnu-gcc; do
  command -v "$x" >/dev/null || { echo "Mangler $x på byggemaskinen" >&2; exit 1; }
done
make -C "$BOARD" cube2v0eu-maskrom-uboot-ums.bin
printf 'Laget RAM-basert U-Boot UMS-loader i %s. Ingen eMMC er skrevet.\n' "$BOARD"
