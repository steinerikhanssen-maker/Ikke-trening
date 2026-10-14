"""Actual Blender inspection of the finished edit and its independently editable shots."""
import bpy,json,sys,hashlib
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
output=Path(sys.argv[sys.argv.index('--')+1]);output.unlink(missing_ok=True)
s=bpy.data.scenes['GYMNOTFOUND_S01E01_EDIT'];checks=[]
def check(name,ok):
    checks.append({'name':name,'status':'PASS' if ok else 'FAIL'})
    assert ok,name
check('360 frames / 12 seconds at 30 fps',(s.frame_start,s.frame_end,s.render.fps)==(1,360,30))
check('native portrait render', (s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage)==(1080,1920,100))
strips=s.sequence_editor.strips if hasattr(s.sequence_editor,'strips') else s.sequence_editor.sequences
shots=sorted([x for x in strips if x.type=='SCENE'],key=lambda x:x.frame_final_start)
check('seven real animated scene strips',len(shots)==7)
check('complete timeline without gaps or overlaps',shots[0].frame_final_start==1 and shots[-1].frame_final_end==361 and all(a.frame_final_end==b.frame_final_start for a,b in zip(shots,shots[1:])))
check('all used image assets embedded',all(i.packed_file for i in bpy.data.images if i.source=='FILE'))
check('all audio stems and mix embedded',all(x.packed_file for x in bpy.data.sounds))
check('relative image and sound references',all(i.filepath.startswith('//') for i in bpy.data.images if i.source=='FILE') and all(x.filepath.startswith('//') for x in bpy.data.sounds))
check('normalized final mix on timeline',any(x.type=='SOUND' and x.name=='NORMALIZED_FINAL_MIX' and not x.mute for x in strips))
identities=[];captions=[]
for strip in shots:
    scene=strip.scene
    check(scene.name+' static shot camera',scene.camera.animation_data is None)
    for obj in scene.objects:
        if obj.name.endswith('_FACE'):
            identities.append(hashlib.sha256(str([tuple(round(v,6) for v in p.co) for p in obj.data.vertices]).encode()).hexdigest())
        if '_CAPTION_' in obj.name and obj.type=='FONT':
            with bpy.context.temp_override(scene=scene,view_layer=scene.view_layers[0]):
                scene.frame_set(obj['caption_start_frame']);scene.view_layers[0].update();graph=bpy.context.evaluated_depsgraph_get()
                evaluated=obj.evaluated_get(graph);camera=scene.camera.evaluated_get(graph)
                points=[world_to_camera_view(scene,camera,evaluated.matrix_world@__import__('mathutils').Vector(c)) for c in evaluated.bound_box]
            bounds=(min(p.x for p in points)*1080,max(p.x for p in points)*1080,(1-max(p.y for p in points))*1920,(1-min(p.y for p in points))*1920)
            check(obj.name+' safe caption bounds',bounds[0]>=72 and bounds[1]<=890 and bounds[2]>=1300 and bounds[3]<=1720)
            captions.append({'text':obj.data.body,'bounds_pixels':bounds})
    arms=[o for o in scene.objects if o.type=='ARMATURE']
    if arms:check(scene.name+' genuinely weighted meshes',all(any(o.type=='MESH' and any(m.type=='ARMATURE' and m.object==a for m in o.modifiers) for o in scene.objects) for a in arms))
check('same Alex face geometry in every appearance',len(identities)==4 and len(set(identities))==1)
check('seven dialogue captions on editable text objects',len(captions)==7)
for n in ['SHOT_04_FOUND_IT','SHOT_05_OFFENDED_TREE']:
    skin=next(o for o in bpy.data.scenes[n].objects if o.name.endswith('_CONTINUOUS_BARK'))
    check(n+' continuous bark deformation',len(skin.data.vertices)>15000 and 'Bark_Jaw_Viseme' in skin.data.shape_keys.key_blocks)
bpy.context.window.scene=s
output.write_text(json.dumps({'blender':bpy.app.version_string,'checks':checks,'captions':captions},indent=2)+'\n');print('PASS',len(checks),'full-project inspections')
