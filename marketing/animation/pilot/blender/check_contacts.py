"""Run in the saved Alex proof; measures evaluated geometry at all 60 frames."""
import bpy,json,sys
from mathutils import Vector
from pathlib import Path
s=bpy.context.scene; arm=bpy.data.objects['ALEX_BODY_ARMATURE']; rows=[]; relative=[]
for f in range(1,61):
    s.frame_set(f); bpy.context.view_layer.update(); graph=bpy.context.evaluated_depsgraph_get()
    ankles={side:list(arm.matrix_world@arm.pose.bones['foot_'+side].head) for side in ['L','R']}
    def center(name):
        ob=bpy.data.objects[name].evaluated_get(graph)
        return ob.matrix_world@(sum((v.co for v in ob.data.vertices),Vector())/len(ob.data.vertices))
    offset=center('PHONE')-center('HAND_L'); relative.append(offset)
    rows.append({'frame':f,'ankles':ankles,'phone_hand_offset':list(offset)})
left=max(abs(r['ankles']['L'][0]+.27) for r in rows)
height=max(abs(r['ankles']['L'][1]+2.10) for r in rows)
right=max(abs(r['ankles']['R'][1]+2.10) for r in rows if r['frame']<=39 or r['frame']>=53)
grip=max((v-relative[0]).length for v in relative)
result={'status':'PASS' if max(left,height,right,grip)<1e-4 else 'FAIL','max_left_x_drift':left,'max_left_height_error':height,'max_right_contact_height_error':right,'max_phone_hand_offset_drift':grip,'frames':rows,'scope':'Geometric contact only; does not establish convincing weight or artistic quality.'}
Path(sys.argv[-1]).write_text(json.dumps(result,indent=2)+'\n')
assert result['status']=='PASS',result
