#!/usr/bin/env bash
# Reproducible, isolated HAOS board-port bootstrap. Does not contact the Cube.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="${1:-$ROOT/work}"
HAOS_COMMIT=bb1dae86266c7ea2759533017e8957a434d50ba0
BOARD_COMMIT=c062a5de84c3bbe8ff47968845f8947442078a32
command -v git >/dev/null || { echo 'git missing' >&2; exit 1; }
command -v python3 >/dev/null || { echo 'python3 missing' >&2; exit 1; }
mkdir -p "$WORK"
checkout_pinned() {
  local url="$1" dir="$2" commit="$3"
  if [[ ! -d "$dir/.git" ]]; then
    [[ ! -e "$dir" ]] || { echo "Existing non-Git directory $dir; abort" >&2; exit 1; }
    git clone "$url" "$dir"
  else
    if [[ -n "$(git -C "$dir" status --porcelain)" ]]; then
      echo "Existing checkout has changes: $dir; refusing to reset" >&2
      exit 1
    fi
  fi
  git -C "$dir" fetch origin "$commit"
  git -C "$dir" checkout --detach "$commit"
  [[ "$(git -C "$dir" rev-parse HEAD)" == "$commit" ]] || { echo "Revision mismatch: $dir" >&2; exit 1; }
}
checkout_pinned 'https://github.com/home-assistant/operating-system.git' "$WORK/operating-system" "$HAOS_COMMIT"
checkout_pinned 'https://github.com/RockPaperPencil/futurehome-cube2v0eu-boardsupport.git' "$WORK/board-support" "$BOARD_COMMIT"
git -C "$WORK/operating-system" submodule update --init --recursive
python3 "$ROOT/scripts/prepare_port.py" --haos "$WORK/operating-system" --board-support "$WORK/board-support"
python3 "$ROOT/scripts/static_preflight.py" "$WORK/operating-system"
printf '\nSource preflight passed. Build: %s/scripts/build.sh %s\n' "$ROOT" "$WORK"
