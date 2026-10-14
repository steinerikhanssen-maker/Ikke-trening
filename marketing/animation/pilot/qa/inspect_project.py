"""Inspect actual revised proof files in Blender. This is technical verification."""
import bpy,sys,json,math
from pathlib import Path
s=bpy.context.scene;out=Path(sys.argv[sys.argv.index('--')+1]);out.unlink(missing_ok=True);checks=[]
def check(name,ok):checks.append({'name':name,'status':'PASS' if ok else 'FAIL'});assert ok,name
check('actual Blender project opens',bool(bpy.data.filepath))
check('native two-second proof', (s.frame_start,s.frame_end,s.render.fps,s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage)==(1,60,30,1080,1920,100))
check('camera remains static',s.camera.animation_data is None)
check('file image assets embedded',all(i.packed_file for i in bpy.data.images if i.source=='FILE'))
check('relative image paths',all(i.filepath.startswith('//') for i in bpy.data.images if i.source=='FILE'))
rigs=[o for o in s.objects if o.type=='ARMATURE']
if rigs:
    arm=rigs[0];check('real multi-bone rig',len(arm.data.bones)>=15)
    weighted=[o for o in s.objects if o.type=='MESH' and any(m.type=='ARMATURE' and m.object==arm for m in o.modifiers)]
    check('actual weighted character geometry',len(weighted)>=15 and all(len(o.vertex_groups)>0 for o in weighted))
    s.frame_set(1);bpy.context.view_layer.update();a=[tuple(v for row in b.matrix for v in row) for b in arm.pose.bones]
    s.frame_set(30);bpy.context.view_layer.update();b=[tuple(v for row in p.matrix for v in row) for p in arm.pose.bones]
    check('poses actually differ',a!=b)
else:
    skin=next(o for o in s.objects if o.name.endswith('_CONTINUOUS_BARK'))
    check('continuous editable bark mesh',len(skin.data.vertices)>15000)
    check('actual knot/brow/jaw shape keys',all(n in skin.data.shape_keys.key_blocks for n in ['Bark_Knots_Open','Offended_Bark_Brows','Bark_Jaw_Viseme']))
    check('no mouth overlay object',not any('MOUTH' in o.name for o in s.objects))
check('all mesh coordinates finite',all(math.isfinite(c) for o in s.objects if o.type=='MESH' for v in o.data.vertices for c in v.co))
out.write_text(json.dumps({'file':Path(bpy.data.filepath).name,'blender':bpy.app.version_string,'checks':checks},indent=2)+'\n');print('PASS',len(checks),'proof-project inspections')
