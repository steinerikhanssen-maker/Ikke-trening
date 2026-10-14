"""Authored character-rig proofs; no storyboard panels are used as frames.
Run Blender 4.3+: blender -b --python blender/build_proofs.py -- NIM
Optional --render writes 60 proof frames. --frame N renders one inspection frame.
All coordinates are editable mesh/curve/armature data in the saved project.
"""
import bpy, math, json, sys, wave
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[1]
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['NIM']
CHAR=args[0]
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for data in list(bpy.data.materials): bpy.data.materials.remove(data)
s=bpy.context.scene
s.render.engine='CYCLES'; s.cycles.samples=8; s.cycles.use_denoising=False
s.cycles.transparent_max_bounces=40
s.render.resolution_x=1080; s.render.resolution_y=1920; s.render.resolution_percentage=100
s.render.fps=30; s.frame_start=1; s.frame_end=60
s.render.image_settings.file_format='PNG'; s.render.film_transparent=False
s.view_settings.view_transform='Standard'
s.world.color=(.04,.04,.04)
bpy.ops.object.camera_add(location=(0,0,20)); cam=bpy.context.object
cam.data.type='ORTHO'; cam.data.ortho_scale=9; s.camera=cam

def rgb(h):
    a=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in a)
def material(name,color):
    m=bpy.data.materials.new(name); m.use_nodes=True; n=m.node_tree.nodes; n.clear()
    out=n.new('ShaderNodeOutputMaterial'); e=n.new('ShaderNodeEmission'); e.inputs[0].default_value=(*rgb(color),1)
    m.node_tree.links.new(e.outputs[0],out.inputs[0]); return m
M={}
def mat(color):
    if color not in M: M[color]=material('COLOR_'+color,color)
    return M[color]
def mesh(name,verts,faces,color):
    d=bpy.data.meshes.new(name); d.from_pydata(verts,[],faces); d.update()
    o=bpy.data.objects.new(name,d); s.collection.objects.link(o); o.data.materials.append(mat(color)); return o

def poly(name,xy,z,color): return mesh(name,[(x,y,z) for x,y in xy],[tuple(range(len(xy)))],color)
def ellipse(name,x,y,rx,ry,z,color):
    return poly(name,[(x+rx*math.cos(i*2*math.pi/48),y+ry*math.sin(i*2*math.pi/48)) for i in range(48)],z,color)
def rectangle(name,x,y,w,h,z,color): return poly(name,[(x-w/2,y-h/2),(x+w/2,y-h/2),(x+w/2,y+h/2),(x-w/2,y+h/2)],z,color)
def capsule(name,x,y,w,h,z,color):
    r=w/2; cy=h/2-r
    points=[(x+r*math.cos(i*math.pi/16),y+cy+r*math.sin(i*math.pi/16)) for i in range(17)]
    points += [(x+r*math.cos(math.pi+i*math.pi/16),y-cy+r*math.sin(math.pi+i*math.pi/16)) for i in range(17)]
    return poly(name,points,z,color)
def line(name,pts,z,width,color):
    d=bpy.data.curves.new(name,'CURVE'); d.dimensions='3D'; d.bevel_depth=width; d.bevel_resolution=3
    sp=d.splines.new('BEZIER'); sp.bezier_points.add(len(pts)-1)
    for p,xy in zip(sp.bezier_points,pts): p.co=(*xy,z); p.handle_left_type=p.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,d); s.collection.objects.link(o); o.data.materials.append(mat(color)); return o

def text(name,body,x,y,size,color,z=2):
    d=bpy.data.curves.new(name,'FONT'); d.body=body; d.size=size; d.align_x='CENTER'
    o=bpy.data.objects.new(name,d); s.collection.objects.link(o); o.location=(x,y,z); d.materials.append(mat(color)); return o

def rig(name,bones):
    d=bpy.data.armatures.new(name); o=bpy.data.objects.new(name,d); s.collection.objects.link(o)
    bpy.context.view_layer.objects.active=o; o.select_set(True); bpy.ops.object.mode_set(mode='EDIT')
    for n,h,t,p in bones:
        b=d.edit_bones.new(n); b.head=h; b.tail=t
        if p: b.parent=d.edit_bones[p]
    bpy.ops.object.mode_set(mode='OBJECT'); o.show_in_front=True
    for b in o.pose.bones: b.rotation_mode='XYZ'
    return o

def bind(obj,arm,bone):
    # Curve drawings stay editable; rigid details follow the same bone as skin meshes.
    if obj.type=='MESH':
        g=obj.vertex_groups.new(name=bone); g.add(list(range(len(obj.data.vertices))),1,'REPLACE')
        m=obj.modifiers.new('CHARACTER_SKIN','ARMATURE'); m.object=arm; obj.parent=arm
    else:
        world=obj.matrix_world.copy(); obj.parent=arm; obj.parent_type='BONE'; obj.parent_bone=bone
        bpy.context.view_layer.update(); obj.matrix_world=world
    return obj

def keyrot(arm,bone,frame,z):
    b=arm.pose.bones[bone]; b.rotation_euler.z=z; b.keyframe_insert('rotation_euler',frame=frame)
def keyloc(arm,bone,frame,x,y):
    b=arm.pose.bones[bone]; b.location=(x,y,0); b.keyframe_insert('location',frame=frame)
def visibility(obj,frames):
    for f,show in frames: obj.hide_render=not show; obj.hide_viewport=not show; obj.keyframe_insert('hide_render',frame=f); obj.keyframe_insert('hide_viewport',frame=f)
def labels(title,sub):
    rectangle('PROOF_TITLE_BAND',0,3.83,8,.74,1.6,'163D35')
    rectangle('PROOF_SCOPE_BAND',0,-3.78,8,.48,1.6,'163D35')
    text('PROOF_TITLE',title,0,3.7,.25,'E5F7EC'); text('PROOF_SCOPE',sub,0,-3.75,.14,'B6D4C3')
rectangle('BACKGROUND',0,0,8,12,-2,'163D35')

if CHAR=='NIM':
    labels('NIM / ACTING STUDY','VOICE AUDITION · lip-sync approval pending')
    manifest=json.loads((ROOT/'assets/nim_rig/rig_manifest.json').read_text())
    bounds=json.loads((ROOT/'assets/nim_rig/layer_bounds.json').read_text())
    bones=[('root',(0,0,0),(0,.5,0),None)]
    names=list(manifest['layer_order'])
    names += [x for family in manifest['variants'].values() for x in family if x not in names]
    for n in names:
        px,py=manifest['pivots_svg_viewbox'].get(n,[120,115]); x,y=(px-120)*.024,(115-py)*.024
        bones.append((n,(x,y,0),(x,y+.2,0),'root'))
    arm=rig('NIM_LAYER_ARMATURE',bones)
    for n in names:
        order=manifest['layer_order'].index(n) if n in manifest['layer_order'] else (8 if 'eyes' in n else 9)
        # Limit transparent mesh area while preserving full-canvas source coordinates,
        # original pivots and original PNG files. Assets are never trimmed/recentered.
        bx0,by0,bx1,by1=bounds[n]
        bx0=max(0,bx0-2); by0=max(0,by0-2); bx1=min(960,bx1+2); by1=min(920,by1+2)
        x0=(bx0/960-.5)*5.76; x1=(bx1/960-.5)*5.76
        y0=(.5-by1/920)*5.52; y1=(.5-by0/920)*5.52
        obj=poly('ART_'+n,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],order*.025,'FFFFFF')
        obj.data.materials.clear()
        img=bpy.data.images.load(str(ROOT/'assets/nim_rig/png'/f'{n}.png')); img.pack()
        m=bpy.data.materials.new('RGBA_'+n); m.use_nodes=True; nodes=m.node_tree.nodes; nodes.clear()
        t=nodes.new('ShaderNodeTexImage'); t.image=img; e=nodes.new('ShaderNodeEmission'); tr=nodes.new('ShaderNodeBsdfTransparent'); mix=nodes.new('ShaderNodeMixShader'); out=nodes.new('ShaderNodeOutputMaterial')
        for a,b in [(t.outputs['Color'],e.inputs[0]),(t.outputs['Alpha'],mix.inputs[0]),(tr.outputs[0],mix.inputs[1]),(e.outputs[0],mix.inputs[2]),(mix.outputs[0],out.inputs[0])]: m.node_tree.links.new(a,b)
        uv=obj.data.uv_layers.new()
        for loop,co in zip(uv.data,[(bx0/960,1-by1/920),(bx1/960,1-by1/920),(bx1/960,1-by0/920),(bx0/960,1-by0/920)]): loop.uv=co
        obj.data.materials.append(m); bind(obj,arm,n)
        if 'eyes' in n:
            active={'08_eyes_neutral':[(1,True),(12,False),(30,True),(40,False),(44,True)],'08_eyes_smug':[(1,False),(12,True),(30,False)],'08_eyes_squint':[(1,False),(40,True),(44,False)]}.get(n,[(1,False)])
            visibility(obj,active)
        if 'mouth' in n:
            seq={ '09_mouth_neutral':[(1,True),(15,False),(33,True)], '09_mouth_mm':[(1,False),(15,True),(19,False)], '09_mouth_ah':[(1,False),(19,True),(23,False)], '09_mouth_smirk':[(1,False),(23,True),(33,False)]}.get(n,[(1,False)])
            visibility(obj,seq)
    for f,x,y,z in [(1,0,0,0),(9,0,-.10,-.04),(15,0,.16,.03),(24,0,.04,-.025),(36,0,0,0),(60,0,0,0)]:
        keyloc(arm,'root',f,x,y); keyrot(arm,'root',f,z)
    for bone,poses in {'03_arm_left':[(1,0),(9,-.12),(17,.38),(30,.25),(48,0),(60,0)],'04_arm_right':[(1,0),(9,.12),(16,-.65),(28,-.52),(44,-.16),(60,0)],'10_antenna':[(1,0),(10,.10),(16,-.12),(23,.075),(32,-.04),(45,0),(60,0)]}.items():
        for f,z in poses: keyrot(arm,bone,f,z)
    for f,v in [(1,(1,1,1)),(9,(1.025,.975,1)),(15,(.98,1.02,1)),(24,(1,1,1)),(60,(1,1,1))]:
        arm.pose.bones['root'].scale=v; arm.pose.bones['root'].keyframe_insert('scale',frame=f)
    s.timeline_markers.new('Anticipation',frame=9); s.timeline_markers.new('Perfect - silent mouth blocking',frame=15); s.timeline_markers.new('Settle',frame=36)

elif CHAR=='Alex':
    labels('ALEX / WEIGHT & STEP','BLOCKING PROOF · character art is not approved')
    rectangle('WALL',0,.8,8,7,-1.8,'D6C5AD'); rectangle('FLOOR',0,-2.9,8,1.7,-1.7,'A5917A')
    rectangle('SOFA_BACK',-.9,-.7,3,1.2,-.8,'476D5E'); rectangle('SOFA_SEAT',-.9,-1.43,3,.36,-.6,'36594C')
    rectangle('SOFA_LEG_L',-2,-1.88,.12,.58,-.8,'483D35'); rectangle('SOFA_LEG_R',.2,-1.88,.12,.58,-.8,'483D35')
    ellipse('CONTACT_SHADOW',.0,-2.23,1.3,.10,-.4,'82715E')
    bones=[('root',(0,-.2,0),(0,.3,0),None),('torso',(0,-.2,0),(0,1.05,0),'root'),('head',(0,1.1,0),(0,1.5,0),'torso'),('thigh_L',(-.24,-.2,0),(-.24,-1.15,0),'root'),('shin_L',(-.24,-1.15,0),(-.24,-2.1,0),'thigh_L'),('foot_L',(-.24,-2.1,0),(.08,-2.1,0),'shin_L'),('thigh_R',(.24,-.2,-.05),(.24,-1.15,-.05),'root'),('shin_R',(.24,-1.15,-.05),(.24,-2.1,-.05),'thigh_R'),('foot_R',(.24,-2.1,-.05),(.55,-2.1,-.05),'shin_R'),('arm_L',(-.46,.92,0),(-.46,.28,0),'torso'),('forearm_L',(-.46,.28,0),(-.46,-.36,0),'arm_L'),('arm_R',(.46,.92,0),(.46,.28,0),'torso'),('forearm_R',(.46,.28,0),(.46,-.36,0),'arm_R')]
    arm=rig('ALEX_BODY_ARMATURE',bones)
    # Distinct, layered authored mesh drawings, not a photographic cutout.
    for side,x,z in [('R',.24,-.1),('L',-.24,.0)]:
        bind(capsule('TROUSER_UPPER_'+side,x,-.68,.38,1.12,z,'78797D'),arm,'thigh_'+side)
        bind(ellipse('KNEE_'+side,x,-1.15,.19,.18,z+.01,'78797D'),arm,'shin_'+side)
        bind(capsule('TROUSER_LOWER_'+side,x,-1.61,.34,1.02,z+.02,'6B6D73'),arm,'shin_'+side)
        bind(poly('SHOE_'+side,[(x-.20,-2.15),(x+.39,-2.15),(x+.39,-2.00),(x-.16,-1.95)],z+.03,'282E32'),arm,'foot_'+side)
        bind(line('TROUSER_SEAM_'+side,[(x-.10,-1.27),(x-.1,-1.94)],z+.03,.012,'A0A1A4'),arm,'shin_'+side)
    bind(poly('HOODIE_TORSO',[(-.43,-.32),(.43,-.32),(.50,.86),(.30,1.06),(-.30,1.06),(-.50,.86)],.2,'30363D'),arm,'torso')
    bind(ellipse('HOOD',0,1.00,.39,.30,.22,'222A30'),arm,'torso')
    bind(rectangle('NECK',0,1.14,.26,.37,.3,'C98B66'),arm,'head')
    for side,x in [('L',-.46),('R',.46)]:
        bone='arm_'+side; low='forearm_'+side
        bind(capsule('SLEEVE_UPPER_'+side,x,.57,.29,.78,.35,'353C44'),arm,bone)
        bind(ellipse('ELBOW_'+side,x,.27,.145,.15,.35,'353C44'),arm,low)
        bind(capsule('SLEEVE_LOWER_'+side,x,-.06,.26,.67,.36,'30373F'),arm,low)
        bind(ellipse('HAND_'+side,x,-.42,.145,.20,.40,'DEA17D'),arm,low)
    bind(ellipse('FACE',0,1.64,.42,.56,.4,'E6AD87'),arm,'head')
    bind(ellipse('EAR_L',-.4,1.6,.12,.16,.42,'D79470'),arm,'head')
    bind(ellipse('EAR_R',.4,1.6,.12,.16,.42,'D79470'),arm,'head')
    hair=[(-.46,1.72),(-.52,2.02),(-.36,2.10),(-.42,2.27),(-.18,2.22),(-.12,2.38),(.08,2.24),(.27,2.34),(.26,2.17),(.48,2.20),(.44,1.75),(.34,1.84),(.28,2.04),(.12,1.97),(-.10,1.93),(-.28,1.85),(-.32,1.67)]
    bind(poly('RUFFLED_HAIR',hair,.46,'332B27'),arm,'head')
    bind(line('HAIR_HIGHLIGHT',[(-.32,2.13),(-.06,2.18),(.14,2.13)],.49,.018,'735442'),arm,'head')
    for x in [-.17,.17]:
        bind(ellipse('EYE_WHITE',x,1.70,.105,.075,.49,'F6E8D9'),arm,'head')
        bind(ellipse('PUPIL',x+.03,1.69,.036,.054,.51,'342D2A'),arm,'head')
        bind(line('BROW',[(x-.10,1.85),(x,1.87),(x+.10,1.83)],.53,.023,'47332A'),arm,'head')
    bind(line('NOSE',[(.04,1.68),(.075,1.52),(.0,1.51)],.52,.012,'B87959'),arm,'head')
    bind(line('MOUTH',[(-.12,1.35),(0,1.37),(.13,1.35)],.53,.015,'815943'),arm,'head')
    for x in [-.17,.17]: bind(line('HOOD_STRING',[(x,1.00),(x,.56)],.45,.012,'9A9C95'),arm,'torso')
    phone=rectangle('PHONE',-.46,-.43,.24,.40,.45,'161F29')
    screen=rectangle('PHONE_SCREEN',-.46,-.42,.19,.30,.46,'70AF9E')
    # Pose solve in XY: sit -> forward COM -> push off -> contact -> passing -> settle.
    # Legs solved from authored hip/ankle targets, preserving foot contact in the rise.
    poses=[(1,-.70,-.76,-.16,[(-.27,-2.04),(.27,-2.04)]),(10,-.70,-.76,-.16,[(-.27,-2.04),(.27,-2.04)]),(19,-.45,-.63,-.27,[(-.27,-2.04),(.27,-2.04)]),(28,-.25,-.22,-.10,[(-.27,-2.04),(.27,-2.04)]),(34,-.12,0,-.025,[(-.27,-2.04),(.27,-2.04)]),(43,.14,.045,-.01,[(-.27,-2.04),(.75,-1.86)]),(50,.39,-.025,0,[(-.15,-2.04),(1.04,-2.04)]),(60,.52,0,0,[(.06,-2.04),(1.04,-2.04)])]
    for f,rx,ry,lean,feet in poses:
        keyloc(arm,'root',f,rx,ry); keyrot(arm,'torso',f,lean); keyrot(arm,'head',f,-lean*.5)
        for side,hx,target in [('L',-.24,feet[0]),('R',.24,feet[1])]:
            hip=Vector((hx+rx,-.2+ry)); foot=Vector(target); delta=foot-hip; dist=min(delta.length,1.899)
            direction=math.atan2(delta.x,-delta.y); flex=math.acos(max(-1,min(1,dist/1.9)))
            thigh=direction+flex; shin=-2*flex
            keyrot(arm,'thigh_'+side,f,thigh); keyrot(arm,'shin_'+side,f,shin)
            # foot bone local orientation differs 90deg; z rotations still compose in XY.
            keyrot(arm,'foot_'+side,f,-thigh-shin)
        for side,up,low in [('L',-.72 if f<19 else -.10,.95 if f<19 else .18),('R',.15 if f<19 else -.10,-.22 if f<19 else .12)]:
            keyrot(arm,'arm_'+side,f,up); keyrot(arm,'forearm_'+side,f,low)
    for f,x in [(1,0),(10,0),(19,.12),(28,0),(60,0)]: keyloc(arm,'head',f,0,x)
    # Bake the hand-held prop transform, then put it on the cushion. No prop vanishing.
    b=arm.data.bones['forearm_L']; s.frame_set(16); bpy.context.view_layer.update()
    release=arm.matrix_world @ arm.pose.bones['forearm_L'].matrix @ b.matrix_local.inverted()
    target=Matrix.Translation(Vector((-1.65,-1.22,.5))) @ Matrix.Rotation(math.pi/2,4,'Z') @ Matrix.Translation(Vector((.46,.43,-.45)))
    for f in range(1,61):
        s.frame_set(f); bpy.context.view_layer.update()
        if f<=16: transform=arm.matrix_world @ arm.pose.bones['forearm_L'].matrix @ b.matrix_local.inverted()
        else: transform=release.lerp(target,min(1,(f-16)/9))
        for obj in [phone,screen]:
            obj.matrix_world=transform
            obj.keyframe_insert('location',frame=f); obj.keyframe_insert('rotation_euler',frame=f)
    for f,title in [(1,'Seated hold'),(19,'Weight over feet'),(34,'Standing'),(43,'Passing pose'),(50,'Heel contact')]: s.timeline_markers.new(title,frame=f)

elif CHAR=='Tree':
    labels('TREE / BARK DEFORMATION','VOICE AUDITION · acting and sync approval pending')
    rectangle('PARK_SKY',0,.3,8,9,-1.8,'A9C6BF'); rectangle('PARK_GROUND',0,-2.9,8,2,-1.7,'82966B')
    ellipse('CANOPY',.0,2.9,2.45,1.1,-.4,'657C52'); ellipse('CANOPY_LIGHT',-.9,3.25,1.6,.8,-.3,'8D9F65')
    # One continuous, editable bark surface; no superimposed mouth plane.
    nx,ny=65,121; verts=[]; faces=[]
    for j in range(ny):
        y=-2.4+j*5.9/(ny-1)
        for i in range(nx):
            u=-1+2*i/(nx-1); width=.90+.08*math.sin(y*2)+.16*math.exp(-((y+2.4)/.45)**2)
            x=u*width+.12*math.sin(y*1.8)
            z=.20*math.sqrt(max(0,1-u*u))+.018*math.sin(u*63+y*2)+.01*math.sin(y*17+u*6)
            verts.append((x,y,z))
    for j in range(ny-1):
        for i in range(nx-1): a=j*nx+i; faces.append((a,a+1,a+nx+1,a+nx))
    trunk=mesh('TREE_CONTINUOUS_BARK_SKIN',verts,faces,'846044')
    for col in ['9A7351','6F503A','A17B56','76543D','B28C62','816044','92704E']: trunk.data.materials.append(mat(col))
    for p in trunk.data.polygons:
        x,y,z=p.center
        # update polygon centers before assigning material stripes
    trunk.data.update()
    for p in trunk.data.polygons:
        x,y,z=p.center; stripe=math.sin(x*25+.65*math.sin(y*1.1))
        p.material_index=1+min(6,int((stripe+1)/2*7)); p.use_smooth=True
    basis=trunk.shape_key_add(name='Basis'); reveal=trunk.shape_key_add(name='Bark_folds_reveal'); speak=trunk.shape_key_add(name='Bark_jaw_speech')
    for k,v in enumerate(verts):
        x,y,z=v
        # Paired knot sockets unfold in the same continuous grid; lips are bark relief.
        eye=0
        for cx in [-.38,.38]:
            r=((x-cx)/.25)**2+((y-.94)/.20)**2; eye+=math.exp(-r*2)
        brow=math.exp(-((y-1.22)/.09)**2)*(math.exp(-((x-.36)/.3)**2)+math.exp(-((x+.36)/.3)**2))
        lip_y=.0-.10*(x/.55)**2
        lip=math.exp(-((y-lip_y)/.045)**2)*math.exp(-(x/.58)**6)
        reveal.data[k].co.z=z-.36*eye+.14*brow+.085*lip
        reveal.data[k].co.y=y+.025*brow
        influence=math.exp(-((y+.04)/.34)**2)*math.exp(-(x/.57)**6)
        speak.data[k].co.y=y+(.065 if y>lip_y else -.065)*influence
        speak.data[k].co.z=z+.12*influence
        # Mouth crease is dark *bark material* on the deforming trunk itself.
    crease=mat('79573B'); trunk.data.materials.append(crease); creaseindex=len(trunk.data.materials)-1
    for p in trunk.data.polygons:
        x,y,z=p.center; lip_y=-.10*(x/.55)**2
        if abs(y-lip_y)<.033 and abs(x)<.58: p.material_index=creaseindex
    # Knot interior eyes are behind, occluded by the continuous bark before reveal.
    for cx in [-.38,.38]:
        ellipse('KNOT_EYE_INTERIOR',cx,.94,.20,.135,-.055,'E4C89B')
        ellipse('KNOT_PUPIL',cx+.02,.92,.055,.095,-.04,'4B4232')
    # Light the bark relief so raised folds read as part of the surface.
    for m in trunk.data.materials:
        nodes=m.node_tree.nodes; emission=next(n for n in nodes if n.type=='EMISSION')
        color=tuple(emission.inputs[0].default_value); nodes.remove(emission)
        bsdf=nodes.new('ShaderNodeBsdfPrincipled'); bsdf.inputs['Base Color'].default_value=color
        bsdf.inputs['Roughness'].default_value=.92
        out=next(n for n in nodes if n.type=='OUTPUT_MATERIAL'); m.node_tree.links.new(bsdf.outputs[0],out.inputs[0])
    s.world.use_nodes=True; s.world.node_tree.nodes['Background'].inputs[0].default_value=(.7,.76,.8,1)
    s.world.node_tree.nodes['Background'].inputs[1].default_value=.55
    bpy.ops.object.light_add(type='AREA',location=(-3,4,7)); lamp=bpy.context.object
    lamp.data.energy=500; lamp.data.shape='DISK'; lamp.data.size=4
    lamp.rotation_euler=(Vector((0,.6,0))-lamp.location).to_track_quat('-Z','Y').to_euler()
    # Branches and bark continuation: original parametric art, not photo planes.
    for name,pts,w in [('LEFT_BRANCH',[(-.65,1.8),(-1.25,2.25),(-1.55,2.65)],.18),('RIGHT_BRANCH',[(.62,2.3),(1.18,2.7),(1.35,3.2)],.20)]:
        line(name,pts,-.07,w,'846044'); line(name+'_RIDGE',[(x+.07,y) for x,y in pts],-.02,.035,'AD8560')
    for f,v in [(1,0),(14,0),(21,1),(27,.95),(42,1),(47,.15),(50,1),(60,.8)]: reveal.value=v; reveal.keyframe_insert('value',frame=f)
    for f,v in [(1,0),(21,0),(26,.7),(30,.25),(34,1),(39,.2),(43,.75),(48,.1),(53,0),(60,0)]: speak.value=v; speak.keyframe_insert('value',frame=f)
    s.timeline_markers.new('Ordinary bark - hold',frame=1); s.timeline_markers.new('Knot eyes unfold',frame=21); s.timeline_markers.new('Speech blocking - no audio',frame=26)
else: raise ValueError(CHAR)

# Refine existing Alex/Tree assets; NIM branch remains untouched.
if CHAR in ('Alex','Tree'):
    exec(compile((ROOT/'blender/refine_characters.py').read_text(), 'refine_characters.py', 'exec'))

# Add the actual local audition as an editable, packed timeline stem. Rendering
# uses the scene directly; FFmpeg muxes this same stem into the proof video.
if CHAR in ['NIM','Tree']:
    audition=ROOT/'audio/voice'/('NIM_01_AUDITION.wav' if CHAR=='NIM' else 'Tree_01_AUDITION.wav')
    if not audition.is_file(): raise FileNotFoundError('Generate local casting auditions before voiced proofs')
    sound=bpy.data.sounds.load(str(audition)); sound.pack()
    editor=s.sequence_editor_create(); strips=editor.strips if hasattr(editor,'strips') else editor.sequences
    strip=strips.new_sound('CASTING_AUDITION_NOT_FINAL',str(audition),channel=1,frame_start=16)
    strip.sound.pack(); s.render.use_sequencer=False
    with wave.open(str(audition),'rb') as wav:
        rate=wav.getframerate(); width=wav.getsampwidth(); channels=wav.getnchannels(); raw=wav.readframes(wav.getnframes())
    samples=[int.from_bytes(raw[i:i+width],'little',signed=True)/(2**(width*8-1)) for i in range(0,len(raw),width*channels)]
    envelope=[]
    for frame in range(1,61):
        begin=max(0,int((frame-16)*rate/30)); end=max(0,int((frame-15)*rate/30))
        segment=samples[begin:end] if frame>=16 else []
        rms=math.sqrt(sum(v*v for v in segment)/max(1,len(segment)))
        envelope.append(rms)
    peak=max(envelope) or 1
    if CHAR=='Tree':
        # One-shot waveform-following jaw deformation, not a perpetual mouth loop.
        for frame,energy in enumerate(envelope,1):
            speak.value=min(1,energy/peak); speak.keyframe_insert('value',frame=frame)
    else:
        mouths={n:bpy.data.objects['ART_'+n] for n in manifest['variants']['mouth']}
        for frame,energy in enumerate(envelope,1):
            active='09_mouth_neutral' if frame<16 else '09_mouth_smirk'
            if energy>peak*.10:
                active='09_mouth_mm' if frame<19 or frame>39 else ('09_mouth_grin' if 31<=frame<=34 else '09_mouth_ah')
            for name,obj in mouths.items():
                obj.hide_render=obj.hide_viewport=(name!=active)
                obj.keyframe_insert('hide_render',frame=frame); obj.keyframe_insert('hide_viewport',frame=frame)
    s['audition_start_frame']=16; s['audition_status']='Local casting candidate; human acting/lip-sync approval NOT TESTED'

# Curves are editable; keep all pictures packed and relative before saving.
s['proof_status']='WORK IN PROGRESS / NOT PUBLICATION READY'
s['voice_status']='Local voice auditions supplied separately. Final acting and lip-sync approval NOT TESTED.'
s['source_provenance']='NIM supplied SVG/PNG; Alex/tree/environment authored by build_proofs.py.'
s['render_version']=bpy.app.version_string
for image in bpy.data.images:
    if image.source=='FILE': image.pack()
edit=ROOT/'edit'; edit.mkdir(exist_ok=True)
s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(edit/f'{CHAR}_PROOF.blend'))
bpy.ops.file.make_paths_relative()
bpy.ops.wm.save_as_mainfile(filepath=str(edit/f'{CHAR}_PROOF.blend'))
frames=ROOT/'renders'/CHAR; frames.mkdir(parents=True,exist_ok=True)
s.render.filepath=str(frames/'frame_')
if '--preview' in args:
    s.render.resolution_percentage=50; s.cycles.samples=32 if CHAR=='Tree' else 8
if '--render' in args: bpy.ops.render.render(animation=True)
if '--frame' in args:
    frame=int(args[args.index('--frame')+1]); s.frame_set(frame); s.render.filepath=str(ROOT/'qa'/f'{CHAR}_{frame:03d}.png'); bpy.ops.render.render(write_still=True)
print('PROOF BUILT:',CHAR, 'Blender',bpy.app.version_string)
