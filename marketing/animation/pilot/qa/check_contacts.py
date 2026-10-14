"""Blender check of real posed prop/foot contact, not a reimplementation of IK."""
import bpy,sys,json,math
from pathlib import Path
s=bpy.context.scene;arm=bpy.data.objects['PROOF_ALEX_RIG'];grip=bpy.data.objects['PROOF_GRIP_ANCHOR'];phone=bpy.data.objects['PROOF_PHONE_PROP']
rows=[]
for frame in range(1,23):
    s.frame_set(frame);bpy.context.view_layer.update()
    distance=(grip.matrix_world.translation.xy-phone.matrix_world.translation.xy).length
    assert distance<.025,(frame,distance)
    rows.append({'frame':frame,'hand_phone_gap':distance})
for frame in range(1,46):
    s.frame_set(frame);bpy.context.view_layer.update()
    for side,expected in [('L',-.25),('R',.20)]:
        foot=bpy.data.objects['PROOF_SHOE_'+side];evaluated=foot.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=evaluated.to_mesh()
        positions=[evaluated.matrix_world@v.co for v in mesh.vertices];sole=min(p.y for p in positions)
        assert abs(sole-(-2.06))<.025,(frame,side,sole)
        # Stable shoe extrema are observed from the evaluated skin mesh itself.
        center=(min(p.x for p in positions)+max(p.x for p in positions))/2
        assert abs(center-(expected+.09))<.025,(frame,side,center)
        evaluated.to_mesh_clear()
output=Path(sys.argv[sys.argv.index('--')+1]);output.write_text(json.dumps({'status':'PASS','hand_frames':22,'plant_frames':45,'tolerance_world_units':.025,'observations':rows},indent=2)+'\n')
print('PASS: 22 hand/phone frames and 90 planted-foot observations')
