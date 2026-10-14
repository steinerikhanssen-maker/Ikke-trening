#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p edit qa/raw-render renders/FINAL final
# Existing licensed stems/fonts/NIM layers are bundled; no network required.
blender -b -t 4 --python blender/create_full_pilot.py > qa/raw-render/build.log 2>&1
test -s edit/edit_timing.json
python3 audio/build_mix.py
# Rebuild once with the final mix packed into the editable timeline.
blender -b -t 4 --python blender/create_full_pilot.py > qa/raw-render/build.log 2>&1
blender -b edit/GymNotFound_S01E01_FINAL.blend -t 4 --python qa/inspect_full_project.py -- qa/full-project-checks.json > qa/raw-render/project-checks.log 2>&1
test -s qa/full-project-checks.json
for character in Alex NIM Tree; do
  blender -b -t 4 --python blender/create_full_pilot.py -- --proof "$character" --render > "qa/raw-render/$character-rev2.log" 2>&1
  case "$character" in Alex) clip=Alex_walk;; NIM) clip=NIM_acting; voice=NIM_01;; Tree) clip=Tree_reveal; voice=Tree_01;; esac
  if [ "$character" = Alex ]; then
    ffmpeg -y -hide_banner -loglevel error -framerate 30 -i "renders/REV2_$character/frame_%04d.png" -frames:v 60 -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart "previews/$clip.mp4"
  else
    ffmpeg -y -hide_banner -loglevel error -framerate 30 -i "renders/REV2_$character/frame_%04d.png" -i "audio/voice/${voice}_AUDITION.wav" -filter_complex '[1:a]adelay=500,apad,atrim=duration=2[a]' -map 0:v -map '[a]' -frames:v 60 -t 2 -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -ar 48000 -b:a 128k -movflags +faststart "previews/$clip.mp4"
  fi
  blender -b "edit/${character}_PROOF.blend" --python qa/inspect_project.py -- "qa/$character-project-checks.json" > "qa/raw-render/$character-inspect.log" 2>&1
  test -s "qa/$character-project-checks.json"
done
blender -b edit/Alex_PROOF.blend --python qa/check_contacts.py -- qa/contact-checks.json > qa/raw-render/contact.log 2>&1
test -s qa/contact-checks.json
blender -b edit/GymNotFound_S01E01_FINAL.blend -t 4 --python-expr "import bpy,time;from pathlib import Path;s=bpy.data.scenes['GYMNOTFOUND_S01E01_EDIT'];bpy.context.window.scene=s;Path('qa/full-render.started').write_text(str(time.time()));s.render.filepath=str(Path('renders/FINAL/frame_').resolve());bpy.ops.render.render(animation=True)" > qa/raw-render/full-render.log 2>&1
python3 blender/export_pilot.py
python3 qa/check_media.py
python3 qa/package_handoff.py
