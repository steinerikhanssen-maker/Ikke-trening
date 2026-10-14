"""Run inside Blender after loading a proof. Assertions are technical, not artistic approval."""
import bpy, json, math, sys
from pathlib import Path
scene=bpy.context.scene
args=sys.argv[sys.argv.index('--')+1:]
output=Path(args[0]); output.unlink(missing_ok=True)
result={'version':bpy.app.version_string,'file':Path(bpy.data.filepath).name,'checks':[]}
def check(name,condition):
    result['checks'].append({'name':name,'status':'PASS' if condition else 'FAIL'})
    if not condition: raise AssertionError(name)
check('editable project opens in actual Blender', bool(bpy.data.filepath))
check('60 frames at 30 fps',scene.frame_start==1 and scene.frame_end==60 and scene.render.fps==30)
check('project configured 1080x1920', (scene.render.resolution_x,scene.render.resolution_y)==(1080,1920))
check('not marked publication ready','NOT PUBLICATION READY' in scene['proof_status'])
check('camera does not substitute for character acting',not scene.camera.animation_data)
check('all external image textures packed',all(i.packed_file for i in bpy.data.images if i.source=='FILE'))
check('relative image references',all(i.filepath.startswith('//') for i in bpy.data.images if i.source=='FILE'))
if scene.get('audition_start_frame'):
    check('audition stem packed in project',len(bpy.data.sounds)>0 and all(sound.packed_file for sound in bpy.data.sounds))
    check('relative sound references',all(sound.filepath.startswith('//') for sound in bpy.data.sounds))
armatures=[o for o in scene.objects if o.type=='ARMATURE']
if armatures:
    arm=armatures[0]
    check('real multi-bone armature',len(arm.data.bones)>=10)
    meshes=[o for o in scene.objects if o.type=='MESH' and any(m.type=='ARMATURE' for m in o.modifiers)]
    check('weighted character meshes',len(meshes)>=10 and all(len(o.vertex_groups)>0 for o in meshes))
    scene.frame_set(1); bpy.context.view_layer.update()
    a=[tuple(value for row in bone.matrix for value in row) for bone in arm.pose.bones]
    scene.frame_set(30); bpy.context.view_layer.update()
    b=[tuple(value for row in bone.matrix for value in row) for bone in arm.pose.bones]
    check('bone poses differ across frames',a!=b)
else:
    trunk=bpy.data.objects.get('TREE_CONTINUOUS_BARK_SKIN')
    check('tree skin is editable connected mesh',trunk is not None and len(trunk.data.vertices)>7000)
    keys=trunk.data.shape_keys.key_blocks
    check('bark reveal and speech are mesh deformations',all(n in keys for n in ['Bark_folds_reveal','Bark_jaw_speech']))
    check('no separate mouth overlay object',not any('MOUTH' in o.name for o in scene.objects))
    check('deformation affects actual vertices',any((v.co-keys['Basis'].data[i].co).length>.04 for i,v in enumerate(keys['Bark_jaw_speech'].data)))
check('all geometry coordinates finite', all(math.isfinite(v) for o in scene.objects if o.type=='MESH' for vert in o.data.vertices for v in vert.co))
output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
