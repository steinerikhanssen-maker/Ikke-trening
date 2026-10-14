#!/usr/bin/env python3
"""Validate the sourced handoff assets. Does not claim Blender runtime or animation quality."""
import json, sys, py_compile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
errors=[]
def test(condition, description):
    print(('PASS' if condition else 'FAIL')+' '+description)
    if not condition: errors.append(description)
for x in ['brief/shot_plan.json','brief/shotlist_30fps.csv','brief/character_bible_no.md','brief/animation_direction_no.md','brief/release_gate_no.md','assets/nim_rig/rig_manifest.json','blender/create_project.py']:
    test((ROOT/x).exists(), 'exists '+x)
rig=json.loads((ROOT/'assets/nim_rig/rig_manifest.json').read_text())
shots=json.loads((ROOT/'brief/shot_plan.json').read_text())
test(shots.get('fps')==30 and shots.get('total_frames')==360, '360 frames / 30 fps plan')
prev=0
for s in shots['shots']:
    test(s['start_f']==prev and s['end_f']>s['start_f'], f'continuous shot {s["shot"]}')
    prev=s['end_f']
test(prev==360, 'shot boundaries end at frame 360')
for name in rig['layer_order'] + rig['variants']['eyes'] + rig['variants']['mouth']:
    for folder,extension in [('png','.png'),('svg','.svg')]:
        test((ROOT/'assets/nim_rig'/folder/(name+extension)).exists(),'rig asset '+folder+'/'+name+extension)
try:
    from PIL import Image
    for name in rig['layer_order'] + rig['variants']['eyes'] + rig['variants']['mouth']:
        p=ROOT/'assets/nim_rig/png'/(name+'.png')
        with Image.open(p) as im: test(im.size==(960,920) and im.mode=='RGBA', 'RGBA 960x920 '+name)
except ImportError:
    print('NOT TESTED PNG dimensions - Pillow not installed')
try:
    py_compile.compile(str(ROOT/'blender/create_project.py'),doraise=True)
    print('PASS Python syntax of Blender starter (NOT Blender runtime)')
except Exception as err:
    test(False,'Blender script syntax: '+str(err))
print(('PASS: handoff assets validated' if not errors else f'FAIL: {len(errors)} error(s)')+'. Blender animation test NOT RUN.')
sys.exit(bool(errors))
