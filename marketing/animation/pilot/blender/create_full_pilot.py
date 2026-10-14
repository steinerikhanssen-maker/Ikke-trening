"""The Ugly Tree: seven editable animated shots, VSE timeline and character proofs.
Blender 4.3.2 tested. Native 1080x1920, 30fps. No storyboard pictures in frames.
"""
import bpy, sys, math, json, wave, os
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,str(Path(__file__).resolve().parent))
from lib.drawing import *
ROOT=Path(__file__).resolve().parents[1]
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
PROOF=args[args.index('--proof')+1] if '--proof' in args else None
bpy.ops.wm.read_factory_settings(use_empty=True)

SHOTS=[('01',1,56,'Apartment'),('02',57,134,'Phone / NIM'),('03',135,150,'Door / shoes'),('04',151,186,'Ugly tree'),('05',187,235,'Tree reveal'),('06',236,316,'Gotcha'),('07',317,360,'GymNotFound')]
DIALOG=[('Alex_01',3,'I hate exercise.'),('NIM_01',58,'Perfect.'),('NIM_02',87,'Find the ugliest tree.'),('Alex_02',151,'Found it.'),('Tree_01',190,'I can hear you.'),('NIM_03',243,'You went outside.'),('NIM_04',282,'Gotcha.')]

@lru_cache(None)
def audio_data(stem):
    p=ROOT/'audio/voice'/f'{stem}_AUDITION.wav'
    with wave.open(str(p),'rb') as w:rate=w.getframerate();width=w.getsampwidth();channels=w.getnchannels();raw=w.readframes(w.getnframes())
    values=[int.from_bytes(raw[i:i+width],'little',signed=True)/2**(width*8-1) for i in range(0,len(raw),width*channels)]
    return rate,values

def energy(stem,seconds):
    if seconds<0:return 0
    rate,data=audio_data(stem);i=int(seconds*rate);section=data[max(0,i-240):i+240]
    return min(1,math.sqrt(sum(x*x for x in section)/max(1,len(section)))/.065)

def dialogue_energy(role,frame):
    return max([energy(stem,(frame-start)/30) for stem,start,_ in DIALOG if stem.startswith(role)] or [0])

def scene(name,start,end,camera=(0,0,20),scale=9):
    s=bpy.data.scenes.new(name);bpy.context.window.scene=s;s.frame_start=start;s.frame_end=end;s.render.engine=os.environ.get('GNF_RENDER_ENGINE','CYCLES');s.cycles.samples=2;s.cycles.use_denoising=False;s.cycles.transparent_max_bounces=16;s.cycles.max_bounces=0
    s.eevee.taa_render_samples=int(os.environ.get('GNF_RENDER_SAMPLES','4'))
    s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.resolution_percentage=100;s.render.fps=30;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard';s.world=bpy.data.worlds.new(name+'_WORLD');s.world.color=(0,0,0)
    bpy.ops.object.camera_add(location=camera);s.camera=bpy.context.object;s.camera.name=name+'_STATIC_CAMERA';s.camera.data.type='ORTHO';s.camera.data.ortho_scale=scale
    return s

def add_caption(s,body,start,end):
    o=text(s.name+f'_CAPTION_{start:03d}',body,-.31,-2.83 if '\n' in body else -2.97,.245,'F7F5E9',15)
    # A solid, quiet plaque keeps text legible without covering the eyes/mouth.
    bg=rect(s.name+f'_CAPTION_BACK_{start:03d}',-.31,-2.86,3.75,.72 if '\n' in body else .5,'183E35',14.9)
    for obj in [o,bg]:hide(obj,s.frame_start,True);hide(obj,start,False);hide(obj,end+1,True)
    o['safe_zone']='Caption bounds x=72..890, y=1500..1645 at 1080x1920, outside right/bottom UI.'
    o['caption_start_frame']=start;o['caption_end_frame']=end
    return [o,bg]

def finish_scene(s):
    s.frame_set(s.frame_start)
    for o in s.objects:linear_action(o)
    for o in s.objects:
        if o.type=='MESH' and o.data.shape_keys:linear_action(o.data.shape_keys)
    s['source']='Authored editable character meshes/curves/armatures. No reference panels used as film frames.'

# Meaningful contact proof: fixed feet until push-off, hand follows the prop until release.
def alex_proof():
    s=scene('PROOF_ALEX',1,60,(-.35,.20,20),6.4);living_room();a=Alex('PROOF')
    for f in range(1,61):
        rx=sample([(1,-.4),(22,-.4),(34,-.18),(43,.0),(50,.12),(60,.42)],f)
        ry=sample([(1,-.75),(22,-.75),(33,-.38),(43,0),(60,0)],f)
        lean=sample([(1,.02),(17,.02),(25,-.13),(34,-.13),(43,-.025),(60,0)],f)
        moving_x=sample([(1,.20),(46,.20),(52,.58),(57,.95),(60,.95)],f)
        moving_y=sample([(1,-1.94),(46,-1.94),(51,-1.62),(57,-1.94),(60,-1.94)],f)
        left_x=sample([(1,-.25),(55,-.25),(60,-.14)],f);left_y=sample([(1,-1.94),(55,-1.94),(60,-1.84)],f)
        px=sample([(1,-.87),(12,-.87),(22,-1.55),(60,-1.55)],f);py=sample([(1,.65),(12,.65),(22,-.06),(60,-.06)],f);pa=sample([(1,-.03),(12,-.03),(22,-math.pi/2),(60,-math.pi/2)],f)
        held=(px,py,pa) if f<=22 else None
        right=(-.10,-.90) if 20<=f<=23 else None
        a.pose(f,root=(rx,ry),lean=lean,feet=[(left_x,left_y),(moving_x,moving_y)],phone=held,hand_r=right,blink=14<=f<=16,look=-.025,headtilt=.025)
        if f>22:a.phone.location=(px,py,0);a.phone.rotation_euler.z=pa;a.phone.keyframe_insert('location',frame=f);a.phone.keyframe_insert('rotation_euler',frame=f)
    s['contact_release_frame']=22;s['plant_end_frame']=45;s['contact_tolerance']=.025
    finish_scene(s);return s

if PROOF:
    if PROOF=='Alex':s=alex_proof()
    elif PROOF=='NIM':
        s=scene('PROOF_NIM',1,60,(0,0,20),6.8);rect('BACKDROP',0,0,8,12,'193F36',-4);n=Nim('PROOF')
        for f in range(1,61):
            t=(f-16)/30;phase='mm' if t<.04 else ('teeth' if .40<t<.63 else 'smug')
            n.pose(f,t,scale=.76,energy=energy('NIM_01',t),phase=phase,gesture=sample([(1,0),(6,0),(10,-.12),(15,1),(31,1),(44,0),(60,0)],f),blink=44<=f<=46)
        finish_scene(s)
    else:
        s=scene('PROOF_TREE',1,60,(0,.45,20),4.7);park();t=Tree('PROOF')
        for f in range(1,61):t.pose(f,reveal=ease((f-11)/7),brow=ease((f-16)/8),speech=energy('Tree_01',(f-16)/30)*.85)
        finish_scene(s)
    for img in bpy.data.images:
        if img.source=='FILE':img.pack()
    s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'edit'/f'{PROOF}_PROOF.blend'));bpy.ops.file.pack_all();bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    if '--frame' in args:
        f=int(args[args.index('--frame')+1]);s.frame_set(f);s.render.filepath=str(ROOT/'qa'/f'{PROOF}_REV2_{f:03d}.png');bpy.ops.render.render(write_still=True)
    if '--render' in args:
        folder=ROOT/'renders'/('REV2_'+PROOF);folder.mkdir(parents=True,exist_ok=True);s.render.filepath=str(folder/'frame_');bpy.ops.render.render(animation=True)
    print('BUILT REVISED PROOF',PROOF);sys.exit(0)

shot_scenes=[]
for number,start,end,description in SHOTS:
    if number=='01':
        s=scene('SHOT_01_APARTMENT',start,end,(-.10,.95,20),4.8);living_room();a=Alex('S01')
        for f in range(start,end+1):a.pose(f,root=(-.40,-.75),lean=.025+.012*math.sin(f*.09),phone=(-.82,.67,-.03),speech=dialogue_energy('Alex',f),blink=25<=f<=28,look=-.025,headtilt=.035)
    elif number=='02':
        s=scene('SHOT_02_PHONE_NIM',start,end,(0,0,20),8.0);rect('ROOM_BOKEH',0,0,8,12,'C7B291',-6)
        # One close-up app prop, editable typography and original NIM rig.
        path('PHONE_HERO',[(-1.35,-2.75),(1.35,-2.75),(1.47,-2.58),(1.47,2.78),(1.32,2.98),(-1.32,2.98),(-1.47,2.78),(-1.47,-2.55)],'253C3B',-.5)
        rect('PHONE_APP_SURFACE',0,.1,2.66,5.34,'F1EDDF',-.3);text('PHONE_EARLY_BRAND','GymNotFound',0,2.48,.24,'1A493D',.5)
        text('PHONE_MISSION','Find the\nugliest tree.',0,-1.47,.23,'1D4C3E',.5);rect('PHONE_MISSION_LINE',0,-.90,2.25,.027,'C8D2C1',.4)
        n=Nim('S02')
        for f in range(start,end+1):
            t=(f-58)/30;en=dialogue_energy('NIM',f);phase='teeth' if .4<t<.63 else 'smug'
            n.pose(f,t,position=(0,.55),scale=.48,energy=en,phase=phase,gesture=sample([(57,0),(60,-.12),(67,1),(93,1),(111,.1),(134,0)],f),blink=118<=f<=120)
    elif number=='03':
        s=scene('SHOT_03_DOOR_STEP',start,end,(.10,-1.20,20),2.5);living_room();a=Alex('S03')
        rect('OPEN_DOOR_FRAME',.94,-.2,.11,5.0,'8C7256',-2.1);rect('OUTSIDE_LIGHT',1.55,.1,1.15,6,'D5DFC8',-2.0)
        for f in range(start,end+1):
            u=(f-start)/(end-start);a.pose(f,root=(-.2+.55*ease(u),-.03*ease(u)),feet=[(-.26,-1.94),(.30+.85*ease(u),-1.94+.32*math.sin(math.pi*u))])
        for o in [a.phone,*a.phone.children]:hide(o,start,True)
    elif number=='04':
        s=scene('SHOT_04_FOUND_IT',start,end,(0,.3,20),7.0);park();t=Tree('S04');t.root.location=(.91,-.25,-.4);t.root.scale=(.61,.61,.61);a=Alex('S04');a.arm.location=(-1.17,-.63,.3);a.arm.scale=(.68,.68,.68);a.phone.location.z=.3
        for f in range(start,end+1):
            a.pose(f,root=(0,0),phone=(-.64,.38,.04),hand_r=(.99,1.25),point=True,speech=dialogue_energy('Alex',f),look=.038,blink=178<=f<=180)
            # Hand controls include a held pointing pose; the body doesn't slide.
            t.pose(f)
        # Static transform for the separately editable held phone matches the character scale.
        a.phone.scale=(.68,.68,.68)
        for f in range(start,end+1):a.phone.location=(-1.17-.64*.68,-.63+.38*.68,.30);a.phone.keyframe_insert('location',frame=f)
    elif number=='05':
        s=scene('SHOT_05_OFFENDED_TREE',start,end,(0,.43,20),4.6);park();t=Tree('S05')
        for f in range(start,end+1):
            t.pose(f,reveal=ease((f-187)/6),brow=ease((f-191)/8),speech=dialogue_energy('Tree',f)*.85)
    elif number=='06':
        s=scene('SHOT_06_GOTCHA',start,end,(0,.45,20),6.3);park();a=Alex('S06');a.arm.location=(-.93,-.50,0);a.arm.scale=(.72,.72,.72);n=Nim('S06')
        for f in range(start,end+1):
            a.pose(f,root=(0,0),phone=(-.61,.50,-.02),look=.035 if f<247 else -.07,blink=248<=f<=250,headtilt=-.015,speech=0)
            a.phone.scale=(.72,.72,.72);a.phone.location=(-.93-.61*.72,-.50+.50*.72,0);a.phone.keyframe_insert('location',frame=f)
            t=(f-243)/30;n.pose(f,t,position=(1.07,-.40),scale=.32,energy=dialogue_energy('NIM',f),phase='smug',gesture=sample([(236,0),(279,0),(282,-.1),(288,1),(301,1),(313,0),(316,0)],f),blink=312<=f<=314)
    else:
        s=scene('SHOT_07_BRAND',start,end,(0,0,20),8.0);rect('BRAND_FIELD',0,0,8,12,'173F35',-4)
        ellipse('BRAND_HALO',0,1.2,1.75,1.58,'245748',-3.9);n=Nim('S07')
        for f in range(start,end+1):n.pose(f,(f-start)/30,position=(0,1.12),scale=.43,phase='neutral',gesture=False,blink=336<=f<=338)
        text('FINAL_BRAND','GymNotFound',0,-.92,.44,'EEF5D9',.8)
        text('FINAL_TAGLINE','Exercise by accident.',0,-1.54,.23,'F2C780',.8)
    # Caption coordinates follow each static camera's framing, on separate source layers.
    for stem,voicestart,body in DIALOG:
        if start<=voicestart<=end:
            rate,values=audio_data(stem);voiceend=min(end,voicestart+math.ceil(len(values)/rate*30)-1)
            # Map master safe-zone positions to shot camera scale and center.
            caption_objects=add_caption(s,body.replace('Find the ugliest tree.','Find the ugliest\ntree.'),voicestart,voiceend)
            for o in caption_objects:
                factor=s.camera.data.ortho_scale/9;o.location.x=o.location.x*factor+s.camera.location.x;o.location.y=o.location.y*factor+s.camera.location.y;o.scale=(factor,factor,factor)
    finish_scene(s);shot_scenes.append(s)

master=scene('GYMNOTFOUND_S01E01_EDIT',1,360);master.render.use_sequencer=True
editor=master.sequence_editor_create();strips=editor.strips if hasattr(editor,'strips') else editor.sequences
for (_,start,end,description),shot in zip(SHOTS,shot_scenes):
    clip=strips.new_scene(shot.name,shot,channel=1,frame_start=start);clip.scene_camera=shot.camera
    master.timeline_markers.new(description,frame=start)
for stem,start,body in DIALOG:
    wav=ROOT/'audio/voice'/f'{stem}_AUDITION.wav';strip=strips.new_sound(stem,str(wav),channel=2,frame_start=start);strip.sound.pack()
# The normalized composite audio is attached once it is generated; separate stems remain editable.
mix=ROOT/'audio/GymNotFound_S01E01_MIX.wav'
if mix.exists():
    sfx=strips.new_sound('EDITABLE_SFX_STEM',str(ROOT/'audio/GymNotFound_S01E01_SFX.wav'),channel=3,frame_start=1);sfx.sound.pack();sfx.mute=True
    stem=strips.new_sound('NORMALIZED_FINAL_MIX',str(mix),channel=4,frame_start=1);stem.sound.pack()
    for strip in strips:
        if strip.channel==2:strip.mute=True
master['duration_seconds']=12.0;master['not_published']=True;master['independent_mobile_and_five_viewer_tests']='NOT TESTED'
master['retiming']='Natural voice durations retained; source shot boundaries retimed, door cut shortened. See edit_timing.json.'
for img in bpy.data.images:
    if img.source=='FILE':img.pack()
master.frame_set(1);bpy.ops.file.pack_all();outfile=ROOT/'edit/GymNotFound_S01E01_FINAL.blend';bpy.ops.wm.save_as_mainfile(filepath=str(outfile));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(outfile))
(ROOT/'edit/edit_timing.json').write_text(json.dumps({'fps':30,'frames':360,'shots':[{'shot':n,'start_frame':a,'end_frame':b,'description':desc} for n,a,b,desc in SHOTS],'dialogue':[{'stem':stem,'start_frame':f,'text':body,'duration_seconds':len(audio_data(stem)[1])/audio_data(stem)[0]} for stem,f,body in DIALOG]},indent=2)+'\n')
if '--frame' in args:
    f=int(args[args.index('--frame')+1]);master.frame_set(f);master.render.filepath=str(ROOT/'qa'/f'FINAL_{f:03d}.png');bpy.ops.render.render(write_still=True)
if '--render' in args:
    folder=ROOT/'renders/FINAL';folder.mkdir(parents=True,exist_ok=True);master.render.filepath=str(folder/'frame_');bpy.ops.render.render(animation=True)
print('CREATED FULL EDIT',outfile)
