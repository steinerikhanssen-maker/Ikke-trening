"""Editable vector art, rigs and deterministic cel materials for the pilot."""
import bpy, math, json
from pathlib import Path
from mathutils import Matrix, Vector
ROOT=Path(__file__).resolve().parents[2]
COLORS={}

def rgb(value):
    c=[int(value[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in c)
def material(color):
    if color in COLORS and COLORS[color].name in bpy.data.materials: return COLORS[color]
    m=bpy.data.materials.new('INK_'+color); m.use_nodes=True; nodes=m.node_tree.nodes;nodes.clear()
    e=nodes.new('ShaderNodeEmission'); e.inputs[0].default_value=(*rgb(color),1)
    out=nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs[0]);COLORS[color]=m;return m

def mesh(name,vertices,faces,color):
    d=bpy.data.meshes.new(name);d.from_pydata(vertices,[],faces);d.update()
    o=bpy.data.objects.new(name,d);bpy.context.scene.collection.objects.link(o);d.materials.append(material(color));return o

def polygon(name,points,color,z=0):return mesh(name,[(x,y,z) for x,y in points],[list(range(len(points)))],color)
def rect(name,x,y,w,h,color,z=0):return polygon(name,[(x-w/2,y-h/2),(x+w/2,y-h/2),(x+w/2,y+h/2),(x-w/2,y+h/2)],color,z)
def ellipse(name,x,y,rx,ry,color,z=0):return polygon(name,[(x+rx*math.cos(i*math.tau/64),y+ry*math.sin(i*math.tau/64)) for i in range(64)],color,z)

def path(name,points,color,z=0,outline=False):
    """Closed Bezier artwork; mesh skin remains genuinely deformable/editable."""
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='2D';d.fill_mode='BOTH';d.resolution_u=12
    sp=d.splines.new('BEZIER');sp.bezier_points.add(len(points)-1);sp.use_cyclic_u=True
    for p,(x,y) in zip(sp.bezier_points,points):p.co=(x,y,0);p.handle_left_type=p.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,d);bpy.context.scene.collection.objects.link(o);o.location.z=z;d.materials.append(material(color))
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH')
    assert len(o.data.polygons)>0, f'Unfilled character art: {name}'
    if outline: stroke(name+'_CONTOUR',points+[points[0]],'302D2A',z-.008,.014)
    return o

def stroke(name,points,color,z=0,width=.012):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.resolution_u=12;d.bevel_depth=width;d.bevel_resolution=2
    sp=d.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
    for p,(x,y) in zip(sp.bezier_points,points):p.co=(x,y,0);p.handle_left_type=p.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,d);bpy.context.scene.collection.objects.link(o);o.location.z=z;d.materials.append(material(color));return o

def text(name,body,x,y,size,color,z=5,bold=True):
    d=bpy.data.curves.new(name,'FONT');d.body=body;d.size=size;d.align_x='CENTER';d.space_line=1.12
    font=ROOT/'assets/fonts'/('OpenSans-Bold.ttf' if bold else 'OpenSans-Regular.ttf')
    if font.exists():d.font=bpy.data.fonts.load(str(font),check_existing=True)
    o=bpy.data.objects.new(name,d);bpy.context.scene.collection.objects.link(o);o.location=(x,y,z);d.materials.append(material(color));return o

def empty(name,location=(0,0,0)):
    o=bpy.data.objects.new(name,None);bpy.context.scene.collection.objects.link(o);o.location=location;return o

def armature(name,bones):
    d=bpy.data.armatures.new(name);a=bpy.data.objects.new(name,d);bpy.context.scene.collection.objects.link(a)
    bpy.ops.object.select_all(action='DESELECT');a.select_set(True);bpy.context.view_layer.objects.active=a;bpy.ops.object.mode_set(mode='EDIT')
    for n,h,t,parent in bones:
        b=d.edit_bones.new(n);b.head=h;b.tail=t
        if parent:b.parent=d.edit_bones[parent]
    bpy.ops.object.mode_set(mode='OBJECT');a.show_in_front=True
    for b in a.pose.bones:b.rotation_mode='XYZ'
    return a

def bind(o,arm,bone):
    bpy.context.view_layer.update()
    world=o.matrix_world.copy()
    if o.type=='CURVE':
        bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH')
    if o.type=='MESH':
        group=o.vertex_groups.new(name=bone);group.add(list(range(len(o.data.vertices))),1,'REPLACE')
        mod=o.modifiers.new('WEIGHTED_CHARACTER_SKIN','ARMATURE');mod.object=arm;o.parent=arm;o.matrix_world=world
    else:
        o.parent=arm;o.parent_type='BONE';o.parent_bone=bone;bpy.context.view_layer.update();o.matrix_world=world
    return o

def key(arm,bone,frame,angle=0,loc=None,scale=None):
    b=arm.pose.bones[bone];b.rotation_euler.z=angle;b.keyframe_insert('rotation_euler',frame=frame)
    if loc is not None:b.location=(*loc,0);b.keyframe_insert('location',frame=frame)
    if scale is not None:b.scale=scale;b.keyframe_insert('scale',frame=frame)

def hide(o,frame,hidden):
    o.hide_render=hidden;o.hide_viewport=hidden;o.keyframe_insert('hide_render',frame=frame);o.keyframe_insert('hide_viewport',frame=frame)

def linear_action(o):
    if o.animation_data and o.animation_data.action:
        for curve in o.animation_data.action.fcurves:
            for p in curve.keyframe_points:p.interpolation='LINEAR'

def ease(t):return max(0,min(1,t))**2*(3-2*max(0,min(1,t)))
def sample(points,f):
    if f<=points[0][0]:return points[0][1]
    for (a,x),(b,y) in zip(points,points[1:]):
        if f<=b:return x+(y-x)*ease((f-a)/(b-a))
    return points[-1][1]
def rotate(x,y,angle):return(x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle))
def solve_two(dx,dy,l1,l2,bend=1):
    d=min(l1+l2-.001,max(abs(l1-l2)+.001,math.hypot(dx,dy)))
    elbow=math.acos(max(-1,min(1,(d*d-l1*l1-l2*l2)/(2*l1*l2))))*bend
    upper=math.atan2(dx,-dy)+math.atan2(l2*math.sin(elbow),l1+l2*math.cos(elbow))
    return upper,-elbow

def feather_arm(m,body):
    """Feather the original arm's proximal artwork into its original body colour."""
    n=m.node_tree.nodes;l=m.node_tree.links
    if n.get('ARM_FOREGROUND_BLEND'):return
    tx=next(x for x in n if x.type=='TEX_IMAGE');e=next(x for x in n if x.type=='EMISSION')
    base=n.new('ShaderNodeTexImage');base.image=body;base.inputs['Vector'].default_value=(174/240,1-116/230,0)
    uv=n.new('ShaderNodeTexCoord');dist=n.new('ShaderNodeVectorMath');dist.operation='DISTANCE';dist.inputs[1].default_value=(174/240,1-116/230,0);l.new(uv.outputs['UV'],dist.inputs[0])
    fade=n.new('ShaderNodeMapRange');fade.inputs['From Min'].default_value=.03;fade.inputs['From Max'].default_value=.14;l.new(dist.outputs['Value'],fade.inputs[0])
    gesture=n.new('ShaderNodeValue');gesture.name='ARM_FOREGROUND_BLEND'
    inverse=n.new('ShaderNodeMath');inverse.operation='SUBTRACT';inverse.inputs[0].default_value=1;l.new(fade.outputs[0],inverse.inputs[1])
    mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';l.new(inverse.outputs[0],mul.inputs[0]);l.new(gesture.outputs[0],mul.inputs[1])
    weight=n.new('ShaderNodeMath');weight.operation='SUBTRACT';weight.inputs[0].default_value=1;l.new(mul.outputs[0],weight.inputs[1])
    mix=n.new('ShaderNodeMixRGB');l.new(weight.outputs[0],mix.inputs[0]);l.new(base.outputs[0],mix.inputs[1]);l.new(tx.outputs['Color'],mix.inputs[2]);l.new(mix.outputs[0],e.inputs[0])

class Nim:
    def __init__(self,prefix):
        self.prefix=prefix;self.art={};manifest=json.loads((ROOT/'assets/nim_rig/rig_manifest.json').read_text());bounds=json.loads((ROOT/'assets/nim_rig/layer_bounds.json').read_text())
        names=manifest['layer_order'][:]
        names += [n for group in manifest['variants'].values() for n in group if n not in names]
        bones=[('root',(0,0,0),(0,.3,0),None)]
        for n in names:
            if 'mouth' in n or 'eyes' in n:
                bx0,by0,bx1,by1=bounds[n];px=(bx0+bx1)/8;py=(by0+by1)/8
            else:px,py=manifest['pivots_svg_viewbox'].get(n,[120,115])
            x,y=(px-120)*.024,(115-py)*.024;bones.append((n,(x,y,0),(x,y+.2,0),'root'))
        self.arm=armature(prefix+'_NIM_RIG',bones)
        body=bpy.data.images.load(str(ROOT/'assets/nim_rig/png/05_body.png'),check_existing=True)
        for n in names:
            layer=manifest['layer_order'].index(n) if n in manifest['layer_order'] else (8 if 'eyes' in n else 9)
            bx0,by0,bx1,by1=bounds[n];bx0=max(0,bx0-2);by0=max(0,by0-2);bx1=min(960,bx1+2);by1=min(920,by1+2)
            x0=(bx0/960-.5)*5.76;x1=(bx1/960-.5)*5.76;y0=(.5-by1/920)*5.52;y1=(.5-by0/920)*5.52
            o=polygon(prefix+'_'+n,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],'FFFFFF',.1+layer*.02)
            uv=o.data.uv_layers.new()
            for item,co in zip(uv.data,[(bx0/960,1-by1/920),(bx1/960,1-by1/920),(bx1/960,1-by0/920),(bx0/960,1-by0/920)]):item.uv=co
            m=bpy.data.materials.new(prefix+'_RGBA_'+n);m.use_nodes=True;nodes=m.node_tree.nodes;nodes.clear();links=m.node_tree.links
            tx=nodes.new('ShaderNodeTexImage');tx.image=bpy.data.images.load(str(ROOT/'assets/nim_rig/png'/f'{n}.png'),check_existing=True)
            emission=nodes.new('ShaderNodeEmission');transparent=nodes.new('ShaderNodeBsdfTransparent');alpha=nodes.new('ShaderNodeMath');alpha.operation='GREATER_THAN';alpha.inputs[1].default_value=.015
            links.new(tx.outputs['Alpha'],alpha.inputs[0]);links.new(tx.outputs['Color'],emission.inputs[0])
            if n in ['06_highlight','07_cheeks']:
                base=nodes.new('ShaderNodeTexImage');base.image=body;mixrgb=nodes.new('ShaderNodeMixRGB');links.new(tx.outputs['Alpha'],mixrgb.inputs[0]);links.new(base.outputs['Color'],mixrgb.inputs[1]);links.new(tx.outputs['Color'],mixrgb.inputs[2]);links.new(mixrgb.outputs[0],emission.inputs[0])
            mix=nodes.new('ShaderNodeMixShader');out=nodes.new('ShaderNodeOutputMaterial')
            links.new(alpha.outputs[0],mix.inputs[0]);links.new(transparent.outputs[0],mix.inputs[1]);links.new(emission.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],out.inputs[0])
            if n=='04_arm_right':feather_arm(m,body)
            o.data.materials.clear();o.data.materials.append(m);bind(o,self.arm,n);self.art[n]=o
        self.arm['design_source']='Original supplied full-canvas NIM SVG/PNG; no redesign.'
    def pose(self,f,time,position=(0,0),scale=.5,energy=0,phase='neutral',gesture=False,blink=False):
        self.arm.location=(*position,0);self.arm.scale=(scale,scale,scale);self.arm.keyframe_insert('location',frame=f);self.arm.keyframe_insert('scale',frame=f)
        g=float(gesture);tilt=-.06*g;key(self.arm,'root',f,tilt,loc=(0,.02*math.sin(time*6)),scale=(1,1,1))
        key(self.arm,'03_arm_left',f,.20*g-.025*(1-g));key(self.arm,'04_arm_right',f,.65*g+.06*(1-g))
        # The leading hand passes in front of the body during the gesture.
        arm_art=self.art['04_arm_right'];arm_art.location.z=.13*max(0,g);arm_art.keyframe_insert('location',frame=f)
        blend=arm_art.data.materials[0].node_tree.nodes.get('ARM_FOREGROUND_BLEND')
        if blend:blend.outputs[0].default_value=max(0,g);blend.outputs[0].keyframe_insert('default_value',frame=f)
        key(self.arm,'10_antenna',f,.10*math.sin(time*12)*math.exp(-max(0,time)*2))
        eye='08_eyes_squint' if blink else ('08_eyes_smug' if phase=='smug' else '08_eyes_neutral')
        mouth='09_mouth_smirk' if phase=='smug' else '09_mouth_neutral'
        if energy>.12:mouth='09_mouth_grin' if phase=='teeth' else '09_mouth_ah'
        if phase=='mm':mouth='09_mouth_mm'
        for n,o in self.art.items():
            if 'eyes' in n:hide(o,f,n!=eye)
            elif 'mouth' in n:hide(o,f,n!=mouth)
            elif n=='00_shadow':hide(o,f,True)
        key(self.arm,'09_mouth_ah',f,scale=(.8,.5+.15*energy,1))

class Alex:
    """Authored adult three-quarter character; every contact is solved per frame."""
    def __init__(self,prefix):
        self.prefix=prefix;self.parts={};self.mouth={};self.eyes=[]
        bones=[('root',(0,0,0),(0,.35,0),None),('torso',(0,0,0),(0,1.35,0),'root'),('head',(0,1.4,0),(0,1.7,0),'torso'),('eyes',(0,2.07,0),(0,2.27,0),'head'),('mouth',(.14,1.65,0),(.14,1.78,0),'head')]
        for side,x in [('L',-.23),('R',.23)]:
            bones += [(f'thigh_{side}',(x,0,0),(x,-1,0),'root'),(f'shin_{side}',(x,-1,0),(x,-2,0),f'thigh_{side}'),(f'foot_{side}',(x,-2,0),(x+.3,-2,0),f'shin_{side}')]
        for side,x in [('L',-.47),('R',.47)]:
            bones += [(f'arm_{side}',(x,1.31,0),(x,.61,0),'torso'),(f'forearm_{side}',(x,.61,0),(x,-.03,0),f'arm_{side}'),(f'hand_{side}',(x,-.03,0),(x,-.23,0),f'forearm_{side}')]
        bones.append(('thumb',(-.55,-.08,0),(-.59,-.18,0),'hand_L'))
        self.arm=armature(prefix+'_ALEX_RIG',bones)
        def draw(bone,name,points,col,z,outline=False):
            before=set(bpy.data.objects);o=path(prefix+'_'+name,points,col,z,outline)
            for p in set(bpy.data.objects)-before:bind(p,self.arm,bone)
            self.parts[name]=o;return o
        def ink(bone,name,points,col,z,width=.012):return bind(stroke(prefix+'_'+name,points,col,z,width),self.arm,bone)
        for side,x,z in [('R',.23,.10),('L',-.23,.14)]:
            draw('thigh_'+side,'TROUSER_UPPER_'+side,[(x-.20,.10),(x+.21,.10),(x+.19,-.92),(x+.08,-1.13),(x-.15,-1.09),(x-.22,-.78)],'737777',z)
            draw('shin_'+side,'TROUSER_LOWER_'+side,[(x-.17,-.91),(x+.17,-.91),(x+.15,-1.90),(x+.10,-2.04),(x-.15,-2.03),(x-.18,-1.70)],'696E6F',z+.02)
            ink('thigh_'+side,'CLOTH_FOLD_'+side,[(x-.16,-.20),(x+.10,-.26),(x+.14,-.34)],'515A5A',z+.04)
            ink('shin_'+side,'TROUSER_SEAM_'+side,[(x-.10,-1.11),(x-.09,-1.53),(x-.10,-1.93)],'919494',z+.045,.009)
            shoe=draw('foot_'+side,'SHOE_'+side,[(x-.18,-2.02),(x-.13,-1.91),(x+.13,-1.94),(x+.37,-2.03),(x+.39,-2.12),(x-.20,-2.12)],'293234',z+.04)
            # Bezier handles must not round the sole below its actual contact plane.
            for vertex in shoe.data.vertices:vertex.co.y=max(vertex.co.y,-2.12)
            ink('foot_'+side,'SOLE_'+side,[(x-.18,-2.10),(x+.14,-2.10),(x+.38,-2.11)],'B1B0A3',z+.055,.012)
            ink('foot_'+side,'LACES_'+side,[(x-.02,-1.99),(x+.08,-2.03),(x+.12,-2.00)],'7F8887',z+.06,.013)
        draw('torso','HOODIE',[(-.34,-.13),(.35,-.13),(.44,.22),(.42,.89),(.53,1.24),(.31,1.45),(-.30,1.45),(-.55,1.24),(-.45,.64)],'343D43',.30,True)
        draw('torso','HOODIE_LIGHT',[(-.30,1.34),(-.42,1.12),(-.39,.30),(-.20,.06),(-.05,.05),(-.07,.62)],'445056',.32)
        draw('torso','HOODIE_SHADOW',[(.27,1.34),(.43,1.08),(.35,.18),(.14,-.08),(.34,-.10),(.44,.68)],'27333A',.33)
        draw('torso','POCKET',[(-.24,.24),(-.13,.44),(.17,.44),(.29,.26),(.24,.15),(-.18,.15)],'303A41',.34)
        ink('torso','POCKET_EDGE',[(-.25,.22),(-.13,.44),(.17,.44),(.29,.22)],'566269',.36)
        ink('torso','HEM',[(-.31,-.08),(.01,-.10),(.34,-.08)],'626B6E',.36,.012)
        draw('torso','HOOD',[(-.33,1.13),(-.41,1.43),(-.27,1.62),(.23,1.62),(.40,1.42),(.28,1.12),(.03,1.02)],'27343B',.38)
        ink('torso','HOOD_EDGE',[(-.29,1.52),(-.25,1.22),(.01,1.12),(.27,1.29),(.27,1.54)],'667078',.40,.014)
        for x in [-.14,.17]:ink('torso','DRAWSTRING',[(x,1.23),(x,.88)],'ADB4B0',.43,.009)
        draw('head','NECK',[(-.19,1.25),(-.20,1.63),(.24,1.69),(.24,1.26),(.04,1.18)],'BE805D',.42)
        for side,x,z in [('R',.47,.36),('L',-.47,.46)]:
            draw('arm_'+side,'SLEEVE_UPPER_'+side,[(x-.15,1.30),(x+.14,1.34),(x+.20,1.15),(x+.15,.66),(x+.05,.50),(x-.13,.57),(x-.19,.86)],'3C484F',z)
            draw('forearm_'+side,'SLEEVE_LOWER_'+side,[(x-.14,.69),(x+.13,.68),(x+.14,.29),(x+.11,-.02),(x-.12,-.04),(x-.15,.20)],'364248',z+.02)
            ink('forearm_'+side,'SLEEVE_FOLD_'+side,[(x-.12,.51),(x+.06,.48),(x+.11,.43)],'58656A',z+.05)
            draw('forearm_'+side,'CUFF_'+side,[(x-.12,.10),(x+.12,.10),(x+.11,-.06),(x-.12,-.06)],'29373E',z+.04)
            hand=draw('hand_'+side,'PALM_'+side,[(x-.11,-.04),(x+.10,-.04),(x+.14,-.11),(x+.12,-.25),(x+.05,-.33),(x-.07,-.31),(x-.14,-.19)],'DCA27B',.80)
            draw('hand_'+side,'PALM_SHADE_'+side,[(x-.12,-.05),(x-.06,-.12),(x-.04,-.27),(x+.08,-.28),(x+.02,-.33),(x-.09,-.28)],'C18B68',.82)
            if side=='R':
                for i in range(3):ink('hand_'+side,'FINGER_'+side+str(i),[(x-.03+i*.045,-.17),(x-.01+i*.04,-.27)],'B67C5A',.86,.007)
            else:
                for i in range(3):
                    yy=-.12-i*.064
                    draw('hand_L','GRIP_FINGER_'+str(i),[(x+.08,yy),(x+.17,yy+.009),(x+.18,yy-.020),(x+.13,yy-.037),(x+.065,yy-.025)],'DDA580',.87)
                    ink('hand_L','GRIP_CREASE_'+str(i),[(x+.10,yy-.025),(x+.155,yy-.025)],'BC815E',.88,.004)
                draw('thumb','GRIPPING_THUMB',[(-.58,-.05),(-.54,-.09),(-.53,-.17),(-.565,-.19),(-.60,-.12)],'E1AD86',.89)
        draw('head','FACE',[(-.38,1.81),(-.38,2.24),(-.22,2.48),(.13,2.49),(.39,2.32),(.41,1.93),(.31,1.65),(.08,1.48),(-.16,1.52),(-.32,1.67)],'E4AC84',.52,True)
        draw('head','FACE_SHADOW',[(-.31,2.23),(-.18,2.25),(-.13,1.86),(-.04,1.62),(.15,1.54),(.06,1.49),(-.17,1.54),(-.34,1.85)],'CF946E',.54)
        draw('head','CHEEK_LIGHT',[(.18,2.05),(.34,2.03),(.31,1.86),(.17,1.77),(.05,1.85)],'EBB88F',.55)
        draw('head','EAR',[(-.37,2.15),(-.51,2.11),(-.51,1.94),(-.39,1.85),(-.32,1.95)],'D69872',.58)
        ink('head','EAR_FOLD',[(-.42,2.08),(-.46,2.04),(-.40,1.98)],'AE704F',.60,.012)
        draw('head','HAIR',[(-.41,2.10),(-.47,2.28),(-.36,2.46),(-.42,2.55),(-.24,2.55),(-.26,2.69),(-.06,2.60),(.05,2.72),(.16,2.61),(.31,2.64),(.30,2.52),(.47,2.43),(.43,2.21),(.35,2.18),(.24,2.40),(.02,2.30),(-.13,2.29),(-.28,2.16),(-.32,1.99)],'332D28',.62,True)
        draw('head','HAIR_LIGHT',[(-.35,2.45),(-.15,2.59),(.04,2.59),(.20,2.49),(.01,2.47),(-.17,2.41)],'4C3B30',.64)
        for points in [[(-.30,2.49),(-.14,2.54),(.04,2.49)],[(-.17,2.34),(.05,2.36),(.22,2.48)],[(.24,2.56),(.36,2.47),(.36,2.32)]]:ink('head','HAIR_STRAND',points,'72523B',.65,.011)
        # Narrow far eye and wider near eye preserve a consistent three-quarter face.
        for name,x,w in [('NEAR',-.08,.14),('FAR',.26,.105)]:
            draw('eyes','EYE_'+name,[(x-w,2.08),(x-.05,2.15),(x+.08,2.14),(x+w,2.08),(x+.05,2.04),(x-.06,2.03)],'F5EBDD',.67)
            self.eyes.append(bind(ellipse(prefix+'_IRIS_'+name,x+.025,2.087,.043,.071,'3B4038',.69),self.arm,'eyes'))
            self.eyes.append(bind(ellipse(prefix+'_PUPIL_'+name,x+.032,2.085,.021,.051,'252C28',.70),self.arm,'eyes'))
            ink('head','LID_'+name,[(x-w,2.09),(x-.03,2.15),(x+w,2.10)],'6D4B39',.72,.012)
            ink('head','BROW_'+name,[(x-w,2.25),(x-.02,2.27),(x+w,2.23)],'42332C',.73,.026)
        ink('head','NOSE_BRIDGE',[(.15,2.13),(.19,1.98),(.26,1.92),(.16,1.91)],'B97D57',.73,.013)
        ink('head','NOSTRIL',[(.19,1.92),(.23,1.90)],'7E533D',.74,.01)
        ink('head','LOWER_LIP',[(.02,1.62),(.11,1.60),(.20,1.62)],'C28D69',.73,.012)
        for name,pts in {'closed':[(-.05,1.68),(.08,1.69),(.24,1.66)],'open':[(-.05,1.69),(.08,1.71),(.24,1.67),(.17,1.59),(.01,1.60)],'teeth':[(-.05,1.69),(.07,1.72),(.24,1.67),(.15,1.65),(.02,1.65)]}.items():
            self.mouth[name]=ink('mouth','MOUTH_'+name,pts,'795440',.75,.009) if name=='closed' else draw('mouth','MOUTH_'+name,pts,'FFF1DB' if name=='teeth' else '684537',.75)
        self.pointer=draw('hand_R','POINTING_INDEX',[(.46,-.23),(.52,-.24),(.52,-.51),(.49,-.56),(.455,-.51)],'DCA27B',.87)
        self.phone=empty(prefix+'_PHONE_PROP')
        before=set(bpy.data.objects)
        path(prefix+'_PHONE_FRAME',[(-.145,-.27),(.145,-.27),(.165,-.24),(.165,.26),(.14,.29),(-.14,.29),(-.165,.25),(-.165,-.24)],'202B2F',.82)
        rect(prefix+'_PHONE_SCREEN',0,.015,.28,.46,'87C7AD',.84)
        text(prefix+'_PHONE_BRAND','GymNotFound',0,.15,.032,'19453A',.86)
        ellipse(prefix+'_PHONE_CAMERA',0,.24,.016,.008,'253633',.86)
        for o in set(bpy.data.objects)-before:o.parent=self.phone
        self.grip=empty(prefix+'_GRIP_ANCHOR',(-.47,-.15,.8));bind(self.grip,self.arm,'hand_L')
        self.arm['character_identity']='Alex: adult, dark hoodie, grey trousers, dark tousled hair. Shared canonical artwork in every shot.'
    def pose(self,f,root=(0,0),lean=0,feet=None,phone=None,hand_r=None,speech=0,blink=False,look=0,headtilt=0,point=False):
        key(self.arm,'root',f,loc=root);key(self.arm,'torso',f,lean);key(self.arm,'head',f,headtilt)
        feet=feet or [(-.23,-1.94),(.23,-1.94)]
        for side,hx,target in [('L',-.23,feet[0]),('R',.23,feet[1])]:
            dx=target[0]-root[0]-hx;dy=target[1]-root[1];upper,lower=solve_two(dx,dy,1,1)
            key(self.arm,'thigh_'+side,f,upper);key(self.arm,'shin_'+side,f,lower);key(self.arm,'foot_'+side,f,-upper-lower)
        for side,x in [('L',-.47),('R',.47)]:
            sx,sy=rotate(x,1.31,lean);sx+=root[0];sy+=root[1]
            angle=phone[2] if side=='L' and phone else (math.pi/2 if side=='R' and point else 0)
            offset=rotate(0,-.12,angle)
            target=(phone[0]-offset[0],phone[1]-offset[1]) if side=='L' and phone else ((hand_r[0]-offset[0],hand_r[1]-offset[1]) if side=='R' and hand_r else (sx+x*.3,sy-1.16))
            upper,lower=solve_two(target[0]-sx,target[1]-sy,.70,.64,1 if side=='R' else -1)
            key(self.arm,'arm_'+side,f,upper-lean);key(self.arm,'forearm_'+side,f,lower)
            key(self.arm,'hand_'+side,f,angle-upper-lower)
        hide(self.pointer,f,not point)
        key(self.arm,'eyes',f,loc=(look,0),scale=(1,.07 if blink else 1,1))
        key(self.arm,'thumb',f,.12*math.sin(f*.6) if f<=10 else 0)
        for n,o in self.mouth.items():hide(o,f,n!=('open' if speech>.25 else 'closed'))
        if phone:
            self.phone.location=(phone[0],phone[1],0);self.phone.rotation_euler=(0,0,phone[2]);self.phone.keyframe_insert('location',frame=f);self.phone.keyframe_insert('rotation_euler',frame=f)

class Tree:
    def __init__(self,prefix):
        self.root=empty(prefix+'_TREE_ROOT');self.prefix=prefix
        before=set(bpy.data.objects)
        nx,ny=97,161;verts=[];faces=[]
        for j in range(ny):
            y=-3+j*8/(ny-1)
            for i in range(nx):
                u=-1+2*i/(nx-1);w=.88+.045*math.sin(y*2.7)+.22*math.exp(-((y+3)/.45)**2)
                x=u*w+.09*math.sin(y*1.6)+.035*y
                z=.34*math.sqrt(max(0,1-u*u))+.016*math.sin(u*61+y*.7)+.01*math.cos(u*41-y*2)
                for cx in [-.36,.36]:z+=.055*math.exp(-((x-cx)/.25)**2-((y-.72)/.16)**2)
                verts.append((x,y,z))
        for j in range(ny-1):
            for i in range(nx-1):a=j*nx+i;faces.append((a,a+1,a+nx+1,a+nx))
        self.skin=mesh(prefix+'_CONTINUOUS_BARK',verts,faces,'96734F');uv=self.skin.data.uv_layers.new()
        for poly in self.skin.data.polygons:
            poly.use_smooth=True
            for li in poly.loop_indices:
                vi=self.skin.data.loops[li].vertex_index;uv.data[li].uv=((vi%nx)/(nx-1),(vi//nx)/(ny-1))
        attr=self.skin.data.color_attributes.new(name='BarkCrease',type='FLOAT_COLOR',domain='POINT')
        basis=self.skin.shape_key_add(name='Basis');self.reveal=self.skin.shape_key_add(name='Bark_Knots_Open');self.brow=self.skin.shape_key_add(name='Offended_Bark_Brows');self.jaw=self.skin.shape_key_add(name='Bark_Jaw_Viseme')
        for i,(x,y,z) in enumerate(verts):
            eyes=sum(math.exp(-(((x-cx)/.245)**4+((y-.72)/.16)**4)*1.4) for cx in [-.36,.36])
            lid=math.exp(-((y-(.91-.16*(1-abs(x)/.65)))/.075)**2)*math.exp(-(x/.78)**8)
            line_y=-.43-.13*(x/.54)**2;crease=math.exp(-((y-line_y)/.021)**2)*math.exp(-(x/.59)**8)
            browline=.95-.20*(1-abs(x)/.68)
            browcrease=math.exp(-((y-browline)/.032)**2)*math.exp(-(x/.75)**8)
            attr.data[i].color=(1-.52*crease,1-.48*browcrease,1,1)
            self.reveal.data[i].co.z=z-.66*eyes
            self.brow.data[i].co.z=z+.21*lid
            self.brow.data[i].co.y=y-.055*lid
            jaw=math.exp(-((y+.43)/.26)**2)*math.exp(-(x/.59)**8)
            self.jaw.data[i].co.y=y+(.07 if y>line_y else -.09)*jaw
            self.jaw.data[i].co.z=z+.055*jaw
        # Stable UV wood texture and cel shading from actual deforming surface normals.
        m=bpy.data.materials.new(prefix+'_PROCEDURAL_WOOD');m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links
        coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(9,1.8,1);l.new(coord.outputs['UV'],mapping.inputs[0])
        noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=5;noise.inputs['Detail'].default_value=4;noise.inputs['Roughness'].default_value=.70;l.new(mapping.outputs[0],noise.inputs[0])
        ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements.remove(ramp.color_ramp.elements[1])
        for index,(at,col) in enumerate([(.15,'644B34'),(.40,'8F6B46'),(.68,'AF8A5D'),(.90,'C6A676')]):
            el=ramp.color_ramp.elements[0] if index==0 else ramp.color_ramp.elements.new(at);el.position=at;el.color=(*rgb(col),1)
        l.new(noise.outputs['Fac'],ramp.inputs[0]);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.04;l.new(noise.outputs['Fac'],bump.inputs['Height'])
        dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=Vector((-.7,.7,1.7)).normalized();l.new(bump.outputs['Normal'],dot.inputs[0])
        shade=n.new('ShaderNodeMapRange');shade.inputs['From Min'].default_value=-1;shade.inputs['From Max'].default_value=1;shade.inputs['To Min'].default_value=.48;shade.inputs['To Max'].default_value=1.08;l.new(dot.outputs['Value'],shade.inputs[0])
        col=n.new('ShaderNodeVertexColor');col.layer_name='BarkCrease';separate=n.new('ShaderNodeSeparateColor');l.new(col.outputs[0],separate.inputs[0])
        self.reveal_ink=n.new('ShaderNodeValue');self.reveal_ink.name='REVEAL_BARK_GROOVE';self.brow_ink=n.new('ShaderNodeValue');self.brow_ink.name='OFFENDED_BARK_GROOVE'
        mouthmix=n.new('ShaderNodeMixRGB');mouthmix.inputs[1].default_value=(1,1,1,1);l.new(self.reveal_ink.outputs[0],mouthmix.inputs[0]);l.new(separate.outputs['Red'],mouthmix.inputs[2])
        browmix=n.new('ShaderNodeMixRGB');browmix.inputs[1].default_value=(1,1,1,1);l.new(self.brow_ink.outputs[0],browmix.inputs[0]);l.new(separate.outputs['Green'],browmix.inputs[2])
        grooves=n.new('ShaderNodeMixRGB');grooves.blend_type='MULTIPLY';grooves.inputs[0].default_value=1;l.new(mouthmix.outputs[0],grooves.inputs[1]);l.new(browmix.outputs[0],grooves.inputs[2])
        mul=n.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;l.new(ramp.outputs[0],mul.inputs[1]);l.new(grooves.outputs[0],mul.inputs[2])
        light=n.new('ShaderNodeMixRGB');light.blend_type='MULTIPLY';light.inputs[0].default_value=1;l.new(mul.outputs[0],light.inputs[1]);l.new(shade.outputs[0],light.inputs[2])
        emission=n.new('ShaderNodeEmission');out=n.new('ShaderNodeOutputMaterial');l.new(light.outputs[0],emission.inputs[0]);l.new(emission.outputs[0],out.inputs[0]);self.skin.data.materials.clear();self.skin.data.materials.append(m)
        for cx in [-.36,.36]:
            ellipse(prefix+'_KNOT_EYE',cx,.72,.245,.138,'DDC7A1',-.08)
            ellipse(prefix+'_IRIS',cx+.018,.705,.053,.079,'4E5138',-.055)
            ellipse(prefix+'_PUPIL',cx+.025,.705,.027,.057,'282F25',-.035)
        for index,points,width in [(0,[(-.50,2.1),(-1.15,2.50),(-1.5,3.17),(-1.8,3.3)],.18),(1,[(.53,2.4),(1.05,2.91),(1.3,3.75),(1.6,3.97)],.23),(2,[(.05,3.6),(-.36,4.30),(-.3,4.85)],.17)]:
            stroke(prefix+'_BRANCH_'+str(index),points,'886844',-.12,width)
            stroke(prefix+'_BRANCH_LIGHT_'+str(index),[(x-.04,y) for x,y in points],'B49265',-.09,width*.18)
        # Layered foliage rather than a single oval canopy.
        for i,(x,y,rx,ry) in enumerate([(-1.7,3.3,.82,.55),(-1.0,4.0,1.0,.65),(-.1,4.7,1.15,.62),(.9,4.2,.85,.65),(1.6,3.8,.93,.55),(.1,3.8,1.25,.7)]):
            ellipse(prefix+'_LEAVES_'+str(i),x,y,rx,ry,['6D8155','889563','9EA772'][i%3],-.30+i*.015)
            for k in range(4):stroke(prefix+'_LEAF_GESTURE',[(x-.35+k*.18,y-.08),(x-.30+k*.18,y+.08)],'A8B079',-.18,.018)
        # Roots remain part of a plausible ordinary crooked tree.
        for i,points in enumerate([[(-.50,-2.65),(-.9,-2.97),(-1.23,-3.04)],[(.48,-2.70),(.83,-2.98),(1.10,-3.05)]]):stroke(prefix+'_ROOT_'+str(i),points,'8C6C49',.02,.13)
        for o in set(bpy.data.objects)-before:o.parent=self.root
        self.skin['mouth_design']='Continuous bark vertex deformation and groove; no overlay/hole object.'
    def pose(self,f,reveal=0,brow=0,speech=0):
        for keyblock,value in [(self.reveal,reveal),(self.brow,brow),(self.jaw,speech)]:keyblock.value=value;keyblock.keyframe_insert('value',frame=f)
        for node,value in [(self.reveal_ink,reveal),(self.brow_ink,brow)]:node.outputs[0].default_value=value;node.outputs[0].keyframe_insert('default_value',frame=f)

def living_room():
    rect('WARM_WALL',0,1,12,12,'E3D3BC',-6);rect('FLOOR',0,-3.9,12,3.68,'B59B7C',-5.8)
    polygon('WINDOW_LIGHT',[(-3.8,-2.07),(-1.6,-2.07),(3.5,-.30),(3.5,1.35)],'CBB293',-5.7)
    rect('WINDOW_TRIM',-2.5,1.8,1.8,3.05,'977E62',-5.5);rect('WINDOW_SKY',-2.5,1.8,1.65,2.89,'BCCDC2',-5.4)
    rect('WINDOW_BAR',-2.5,1.8,.045,2.95,'E7D8BE',-5.3);rect('WINDOW_MIDDLE',-2.5,1.8,1.68,.045,'E7D8BE',-5.3)
    rect('SKIRTING',0,-2.0,10,.09,'947C64',-5.4)
    path('SOFA_BACK',[(-1.65,-.97),(-1.75,.03),(-1.5,.27),(.52,.27),(.72,.07),(.65,-.97)],'527568',-1.6)
    path('SOFA_LEFT_CUSHION',[(-1.55,-.77),(-1.58,.10),(-.65,.10),(-.55,-.82)],'638273',-1.55)
    path('SOFA_RIGHT_CUSHION',[(-.51,-.82),(-.47,.11),(.56,.06),(.58,-.79)],'55776A',-1.54)
    path('SOFA_SEAT',[(-1.61,-.91),(.58,-.91),(.68,-1.08),(.56,-1.25),(-1.64,-1.25)],'3E6659',-1.15)
    for x in [-1.49,.49]:rect('SOFA_LEG',x,-1.58,.10,.80,'554535',-1.7)
    ellipse('SOFA_SHADOW',-.5,-2.03,1.7,.09,'9F886B',-2.0)
    rect('SIDE_TABLE_LEG',-1.55,-1.16,.09,1.65,'6F5842',-1.0);ellipse('TABLE_TOP',-1.55,-.31,.52,.10,'8B6B4E',-.95)
    rect('LAMP_STAND',1.58,.05,.05,3.6,'A28765',-3);ellipse('LAMP_BASE',1.58,-1.7,.35,.07,'A28765',-3)
    polygon('LAMP_SHADE',[(1.09,1.72),(1.24,2.35),(1.87,2.35),(2.05,1.72)],'F1DEAC',-2.9)
    stroke('LAMP_EDGE',[(1.09,1.72),(1.55,1.65),(2.05,1.72)],'D6BD88',-2.8,.014)
    rect('ART_FRAME',.72,2.35,.73,.88,'9B8266',-5.2);rect('ART_PAPER',.72,2.35,.65,.80,'F6EAD4',-5.1)
    ellipse('ART_CIRCLE',.69,2.39,.19,.20,'C18E65',-5);stroke('ART_STEM',[(.47,2.16),(.64,2.33),(.91,2.14)],'718365',-4.9,.018)

def park():
    rect('SKY',0,1,16,14,'CFDED2',-7);rect('PARK_GROUND',0,-4,16,4,'909F77',-6.7)
    for x,y,rx in [(-2.1,3.1,1.1),(1.8,3.5,1.4)]:
        path('CLOUD',[(x-rx,y),(x-.6*rx,y+.12),(x-.45*rx,y+.35),(x-.15*rx,y+.28),(x+.18*rx,y+.39),(x+.62*rx,y+.18),(x+rx,y)],'E9EBD9',-6.8)
    for i,x in enumerate([-3.0,-1.7,.0,1.7,3.0]):
        rect('NEIGHBOUR_HOUSE',x,-.19,1.15,1.60,['BECAB5','D9CFB5','C0CDBA'][i%3],-6.4)
        polygon('HOUSE_ROOF',[(x-.72,.56),(x,.99),(x+.70,.56)],'94A799',-6.3)
        for k in [-.27,.27]:rect('HOUSE_WINDOW',x+k,-.05,.24,.37,'8D9E8C',-6.2)
    path('PARK_PATH',[(-2.5,-4.6),(2.0,-4.6),(.6,-1.3),(-.04,-1.3)],'CDC5AC',-6)
    rect('FENCE_RAIL',0,-1.33,10,.08,'9EA888',-5.9)
    for x in range(-5,6):rect('FENCE_POST',x*.6,-1.61,.07,.83,'9EA888',-5.8)
    for x,y in [(-2.4,-2.13),(1.75,-2.18),(-1.65,-2.8),(2.1,-3.1)]:
        for k in range(3):stroke('GRASS',[(x+k*.08,y),(x+k*.08-.04,y+.14)],'637D54',-5.1,.011)
