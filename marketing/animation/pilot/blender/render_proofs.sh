#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p qa/raw-render previews
for character in NIM Alex Tree; do
  python3 - "$character" <<'PY'
from pathlib import Path
import sys, time
(Path('qa/raw-render')/f'{sys.argv[1]}.started').write_text(str(time.time()))
PY
  blender -b -t 6 --python blender/build_proofs.py -- "$character" --preview --render > "qa/raw-render/$character-render.log" 2>&1
  # A Blender process may exit zero after a Python exception. Verify every output frame.
  python3 - "$character" <<'PY'
from pathlib import Path
import sys
folder=Path('renders')/sys.argv[1]
assert all((folder/f'frame_{i:04d}.png').is_file() for i in range(1,61)), 'Incomplete render'
started=float((Path('qa/raw-render')/f'{sys.argv[1]}.started').read_text())
assert all((folder/f'frame_{i:04d}.png').stat().st_mtime>=started for i in range(1,61)), 'Stale frames from a previous render'
raw=(Path('qa/raw-render')/f'{sys.argv[1]}-render.log').read_text()
lines=[line for line in raw.splitlines() if line.startswith(('Info:','Saved:','Time:','PROOF BUILT:','Blender ')) or 'Error:' in line or 'Traceback' in line]
(Path('qa')/f'{sys.argv[1]}-render.log').write_text('\n'.join(lines)+'\n')
PY
  case "$character" in
    NIM) clip=NIM_acting;;
    Alex) clip=Alex_walk;;
    Tree) clip=Tree_reveal;;
  esac
  if [ "$character" = Alex ]; then
    ffmpeg -y -hide_banner -loglevel error -framerate 30 -i "renders/$character/frame_%04d.png" -frames:v 60 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -movflags +faststart "previews/$clip.mp4"
  else
    if [ "$character" = NIM ]; then voice=NIM_01; else voice=Tree_01; fi
    ffmpeg -y -hide_banner -loglevel error -framerate 30 -i "renders/$character/frame_%04d.png" -i "audio/voice/${voice}_AUDITION.wav" -filter_complex '[1:a]adelay=500,apad,atrim=duration=2[a]' -map 0:v -map '[a]' -frames:v 60 -t 2 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -ar 48000 -b:a 128k -movflags +faststart "previews/$clip.mp4"
  fi
  blender -b "edit/${character}_PROOF.blend" --python blender/inspect_project.py -- "qa/$character-project-checks.json" > "qa/$character-reopen.log" 2>&1
  test -s "qa/$character-project-checks.json"
done
python3 qa/check_media.py
