"""M1 revision: applied to the existing rig/mesh, never to NIM.
Executed in build_proofs' namespace so original editable assets stay authoritative.
"""
if CHAR == 'Alex':
    arm.animation_data_clear()
    for bone in arm.pose.bones:
        bone.matrix_basis=Matrix.Identity(4)
    bpy.context.view_layer.update()
    bpy.data.objects['PROOF_SCOPE'].data.body='M1 REVISION · contact / weight / acting study'
    bpy.context.view_layer.objects.active=arm
    bpy.ops.object.mode_set(mode='EDIT')
    wrist=arm.data.edit_bones.new('hand_L'); wrist.head=(-.46,-.42,0); wrist.tail=(-.46,-.62,0); wrist.parent=arm.data.edit_bones['forearm_L']
    bpy.ops.object.mode_set(mode='OBJECT'); arm.pose.bones['hand_L'].rotation_mode='XYZ'
    hand=bpy.data.objects['HAND_L']; hand.modifiers.clear(); hand.vertex_groups.clear(); bind(hand,arm,'hand_L')
    # Tailored silhouette, fabric overlap and restrained warm/cool modelling.
    bind(poly('HOODIE_SIDE_SHADOW',[(-.43,-.32),(-.28,-.31),(-.32,.53),(-.46,.82)],.225,'202A32'),arm,'torso')
    bind(poly('HOODIE_CHEST_LIGHT',[(-.29,.78),(.25,.84),(.34,.58),(.27,.12),(-.24,.16)],.23,'3E4B55'),arm,'torso')
    bind(line('POCKET_WELT',[(-.27,-.04),(-.18,.10),(.17,.10),(.28,-.04)],.25,.018,'1C252D'),arm,'torso')
    bind(line('HOODIE_HEM',[(-.40,-.27),(0,-.30),(.40,-.27)],.26,.028,'202A32'),arm,'torso')
    bind(poly('FACE_SIDE_PLANE',[(.25,2.01),(.39,1.87),(.41,1.60),(.29,1.26),(.10,1.11),(.22,1.49)],.445,'D39471'),arm,'head')
    bind(ellipse('CHEEK_WARMTH',-.26,1.49,.10,.055,.455,'DF9C7C'),arm,'head')
    bind(line('LOWER_LIP',[(-.07,1.30),(.02,1.29),(.10,1.31)],.54,.012,'C68B6D'),arm,'head')
    for side,x in [('L',-.24),('R',.24)]:
        bind(line('SHOE_SOLE_'+side,[(x-.18,-2.145),(x+.16,-2.145),(x+.37,-2.145)],.16,.025,'C7C4B6'),arm,'foot_'+side)
        for j in range(3): bind(line('LACE_'+side+str(j),[(x+.02+j*.065,-2.035),(x+.065+j*.065,-2.07)],.17,.009,'9CABA6'),arm,'foot_'+side)
    # Prop stays gripped throughout this rise/step study. No unsupported throw
    # to the cushion: that separate acting beat is explicitly deferred.
    for ob in [phone,screen]:
        ob.animation_data_clear(); ob.matrix_world=Matrix.Identity(4); bind(ob,arm,'hand_L')
    bind(rectangle('PHONE_CAMERA',-.46,-.27,.07,.018,.47,'233D3B'),arm,'hand_L')
    for i in range(3):
        bind(line('GRIP_FINGER_'+str(i),[(-.59,-.35-i*.055),(-.53,-.365-i*.055),(-.51,-.38-i*.055)],.49,.025,'E6AD87'),arm,'hand_L')
    bind(line('GRIP_THUMB',[(-.35,-.54),(-.33,-.43),(-.38,-.40)],.50,.035,'F0BB95'),arm,'hand_L')
    # Bake analytic two-link legs at every frame. Interpolating joint angles
    # between sparse poses caused foot drift in the earlier proof.
    keys=[(1,-.70,-.76,-.10,-.27,.27,0),(10,-.70,-.78,-.14,-.27,.27,0),
          (20,-.43,-.69,-.23,-.27,.27,0),(34,-.08,-.06,-.04,-.27,.27,0),
          (39,-.02,-.09,-.02,-.27,.27,0),(46,.12,-.06,-.015,-.27,.73,.24),
          (53,.28,-.13,0,-.27,1.04,0),(60,.30,-.15,0,-.27,1.04,0)]
    arm.animation_data_clear()
    for f in range(1,61):
        a,b=next((a,b) for a,b in zip(keys,keys[1:]) if a[0]<=f<=b[0])
        t=(f-a[0])/(b[0]-a[0]); t=t*t*(3-2*t)
        rx,ry,lean,lx,rxfoot,lift=[a[i]+(b[i]-a[i])*t for i in range(1,7)]
        keyloc(arm,'root',f,rx,ry); keyrot(arm,'torso',f,lean); keyrot(arm,'head',f,-lean*.65)
        for side,hx,fx,fy in [('L',-.24,lx,-2.10),('R',.24,rxfoot,-2.10+lift)]:
            d=Vector((fx-hx-rx,fy+.2-ry)); distance=d.length
            if distance>1.9: raise ValueError('Unreachable planted foot at frame '+str(f))
            flex=math.acos(distance/1.9); angle=math.atan2(d.x,-d.y)+flex
            keyrot(arm,'thigh_'+side,f,angle); keyrot(arm,'shin_'+side,f,-2*flex)
            keyrot(arm,'foot_'+side,f,-angle+2*flex)
        keyrot(arm,'arm_L',f,-.30); keyrot(arm,'forearm_L',f,2.1)
        keyrot(arm,'hand_L',f,-1.8-lean)
        keyrot(arm,'arm_R',f,.08+lean*.7); keyrot(arm,'forearm_R',f,-.12)
    for fc in arm.animation_data.action.fcurves:
        for k in fc.keyframe_points: k.interpolation='LINEAR'
    s['contact_revision']='Phone retained in grip; fixed left sole, right step lands at frame 53; per-frame analytic legs.'
    s.timeline_markers.clear()
    for f,n in [(1,'Seated / phone grip'),(20,'Anticipation / forward weight'),(34,'Rise'),(46,'Right foot passing'),(53,'Right foot planted'),(60,'Weight settles')]: s.timeline_markers.new(n,frame=f)

elif CHAR == 'Tree':
    bpy.data.objects['PROOF_SCOPE'].data.body='M1 REVISION · offended reaction / organic bark'
    # A continuous procedural shader replaces polygon-wise colour bands.
    bark=bpy.data.materials.new('BARK_ORGANIC_CONTINUOUS'); bark.use_nodes=True
    ns=bark.node_tree.nodes; ns.clear(); links=bark.node_tree.links
    out=ns.new('ShaderNodeOutputMaterial'); bs=ns.new('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value=.86
    tex=ns.new('ShaderNodeTexCoord'); scale=ns.new('ShaderNodeVectorMath'); scale.operation='MULTIPLY'; scale.inputs[1].default_value=(5,.65,2)
    noise=ns.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value=3; noise.inputs['Detail'].default_value=3; noise.inputs['Roughness'].default_value=.7
    ramp=ns.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position=.20; ramp.color_ramp.elements[0].color=(*rgb('513B30'),1)
    ramp.color_ramp.elements[1].position=.80; ramp.color_ramp.elements[1].color=(*rgb('B89366'),1)
    bump=ns.new('ShaderNodeBump'); bump.inputs['Strength'].default_value=.22; bump.inputs['Distance'].default_value=.055
    for a,b in [(tex.outputs['Object'],scale.inputs[0]),(scale.outputs[0],noise.inputs['Vector']),(noise.outputs['Fac'],ramp.inputs[0]),(ramp.outputs[0],bs.inputs['Base Color']),(noise.outputs['Fac'],bump.inputs['Height']),(bump.outputs[0],bs.inputs['Normal']),(bs.outputs[0],out.inputs[0])]: links.new(a,b)
    trunk.data.materials.append(bark); bi=len(trunk.data.materials)-1
    for p in trunk.data.polygons:
        if p.material_index!=creaseindex: p.material_index=bi
    # Bark sockets, heavy asymmetric brows, sideways glance, long offended hold.
    # Details are relief curves, not a rectangular face decal.
    for ob in list(s.objects):
        if ob.name.startswith(('KNOT_EYE_INTERIOR','KNOT_PUPIL')): bpy.data.objects.remove(ob,do_unlink=True)
    for side,cx in [('L',-.38),('R',.38)]:
        eye=ellipse('KNOT_SOCKET_'+side,cx,.96,.29,.23,.31,'49382B')
        white=ellipse('KNOT_EYE_'+side,cx,.96,.23,.16,.34,'E7D6AF')
        pupil=ellipse('KNOT_GAZE_'+side,cx-.055,.95,.063,.11,.36,'302C25')
        glint=ellipse('KNOT_GLINT_'+side,cx-.075,.99,.018,.027,.38,'FFF0CB')
        brow=line('BARK_BROW_'+side,[(cx-.27,1.19),(cx,1.24),(cx+.25,1.17)],.40,.075,'523C2D')
        ridge=line('BROW_LIGHT_'+side,[(cx-.25,1.23),(cx,1.28),(cx+.23,1.21)],.42,.018,'BC9767')
        lid=line('BARK_LID_'+side,[(cx-.24,1.02),(cx,1.06),(cx+.23,1.02)],.40,.038,'755638')
        for ob in [eye,white,pupil,glint,brow,ridge,lid]:
            visibility(ob,[(1,False),(17,True)])
            for f,y in [(1,-.12),(17,-.12),(23,.02 if side=='L' else -.09),(30,0 if side=='L' else -.065),(60,0 if side=='L' else -.065)]:
                ob.location.y=y; ob.keyframe_insert('location',frame=f)
        for ob in [pupil,glint]:
            for f,x in [(17,0),(25,-.04),(36,-.04),(44,.02),(60,.02)]: ob.location.x=x; ob.keyframe_insert('location',frame=f)
    # Carve a downward-turning mouth directly into the existing skin.
    for p in trunk.data.polygons:
        x,y,z=p.center
        if abs(x)<.57 and abs(y-(.08-.30*(x/.57)**2))<.045: p.material_index=creaseindex
        elif p.material_index==creaseindex: p.material_index=bi
    crease.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*rgb('352B24'),1)
    for idx,v in enumerate(verts):
        x,y,z=v
        if abs(y)<.4:
            influence=math.exp(-((y-.04)/.3)**2)*math.exp(-(x/.57)**6)
            speak.data[idx].co.y=y+(.09 if y>.04 else -.09)*influence
    for f,v in [(1,0),(14,0),(23,1),(60,1)]: reveal.value=v; reveal.keyframe_insert('value',frame=f)
    s['acting_revision']='Asymmetric bark brows, sideways gaze, downturned carved mouth; expression holds after reveal.'

    # Continuous object-space mouth mask avoids pixelated per-face colouring.
    for p in trunk.data.polygons: p.material_index=bi
    xyz=ns.new('ShaderNodeSeparateXYZ'); links.new(tex.outputs['Object'],xyz.inputs[0])
    def mathnode(op,a,b):
        n=ns.new('ShaderNodeMath'); n.operation=op
        for i,v in enumerate((a,b)):
            if isinstance(v,(int,float)): n.inputs[i].default_value=v
            else: links.new(v,n.inputs[i])
        return n
    xx=mathnode('MULTIPLY',xyz.outputs['X'],xyz.outputs['X'])
    curve=mathnode('MULTIPLY',xx.outputs[0],.923)
    yy=mathnode('ADD',xyz.outputs['Y'],curve.outputs[0])
    center=mathnode('SUBTRACT',yy.outputs[0],.08)
    absolute=mathnode('ABSOLUTE',center.outputs[0],0)
    band=mathnode('LESS_THAN',absolute.outputs[0],.025)
    driver=band.inputs[1].driver_add('default_value').driver
    driver.expression='.025+.065*v'; var=driver.variables.new(); var.name='v'; var.type='SINGLE_PROP'
    var.targets[0].id_type='KEY'; var.targets[0].id=trunk.data.shape_keys; var.targets[0].data_path='key_blocks["Bark_jaw_speech"].value'
    ax=mathnode('ABSOLUTE',xyz.outputs['X'],0); limit=mathnode('LESS_THAN',ax.outputs[0],.57)
    mask=mathnode('MULTIPLY',band.outputs[0],limit.outputs[0])
    mix=ns.new('ShaderNodeMixRGB'); links.new(mask.outputs[0],mix.inputs[0]); links.new(ramp.outputs[0],mix.inputs[1]); mix.inputs[2].default_value=(*rgb('352B24'),1)
    links.new(mix.outputs[0],bs.inputs['Base Color'])
    s.cycles.samples=32
