#!/usr/bin/env bash
# RAUC bundle cryptographic verification and board compatibility gate.
set -euo pipefail
[[ $# -eq 2 ]] || { echo 'Usage: verify_update.sh BUNDLE.raucb TRUSTED-CERT-OR-KEYRING.pem' >&2; exit 2; }
BUNDLE="$1"; KEYRING="$2"
[[ -s "$BUNDLE" && -s "$KEYRING" ]] || { echo 'Missing RAUC bundle or trust keyring' >&2; exit 2; }
[[ "$(basename "$BUNDLE")" == haos_cube2v0eu-*.raucb ]] || { echo 'Not a Cube bundle' >&2; exit 2; }
command -v rauc >/dev/null || { echo 'Install RAUC on the verification PC; refuse unchecked update' >&2; exit 2; }
INFO="$(rauc info --keyring="$KEYRING" "$BUNDLE")" || { echo 'RAUC signature verification failed' >&2; exit 1; }
# Check the manifest output for the exact board identity; `rauc info` verifies
# signature using the passed trust keyring when configured.
if ! grep -Eiq "compatible[[:space:]]*:[[:space:]]*['\"]?haos-cube2v0eu['\"]?([[:space:]]|$)" <<< "$INFO"; then
  echo 'Incompatible RAUC bundle (expected haos-cube2v0eu)' >&2; exit 1
fi
printf 'RAUC bundle signature and board compatibility checked.\n%s\n' "$INFO"
