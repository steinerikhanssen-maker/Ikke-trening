"""GymNotFound S01E01: create a clean Blender scene with frame markers and the layered NIM source rig.

Blender executable required. Run:
    blender -b --python blender/create_project.py

This is a technical STARTING POINT for an animator/Codex. It does NOT produce a finished
animated scene or a publication-grade video. It needs backgrounds, characters, acting,
voice tracks, camera blocking and QA. Tested by Python compile; not run against bpy here.
"""
import json
import math
from pathlib import Path
import bpy

ROOT = Path(__file__).resolve().parent.parent
RIG = ROOT / 'assets' / 'nim_rig'
CONFIG = json.loads((ROOT / 'brief' / 'shot_plan.json').read_text(encoding='utf8'))
MANIFEST = json.loads((RIG / 'rig_manifest.json').read_text(encoding='utf8'))

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

scene = bpy.context.scene
try:
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
except (TypeError, ValueError):
    try:
        scene.render.engine = 'BLENDER_EEVEE'
    except (TypeError, ValueError):
        scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100
scene.render.fps = 30
scene.render.fps_base = 1
scene.frame_start = 1
scene.frame_end = 360
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = str(ROOT / 'renders' / 'nim_previs_')
scene.view_settings.view_transform = 'Standard'

# Named markers are editable and correspond to first frames of the shots.
for shot in CONFIG['shots']:
    mark = scene.timeline_markers.new(f"SHOT_{shot['shot']}_{shot['set']}", frame=shot['start_f'] + 1)

bpy.ops.object.camera_add(location=(0, 0, 18))
cam = bpy.context.object
cam.name = 'CAM_MAIN_VERTICAL'
cam.data.type = 'ORTHO'
cam.data.ortho_scale = 9.0
scene.camera = cam

bpy.ops.object.empty_add(type='PLAIN_AXES')
root = bpy.context.object
root.name = 'NIM_ROOT__MOVE_THIS_TO_SHOT'
root.location = (0, 0, 0)
root.scale = (1, 1, 1)

# Import each transparent full-canvas SVG render on a color/alpha-preserving plane.
# Pivot controls are separate transform empties; planes remain aligned on the same source canvas.
def image_material(image_path, name):
    img = bpy.data.images.load(str(image_path), check_existing=True)
    mat = bpy.data.materials.new('MAT_' + name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    emission = nodes.new('ShaderNodeEmission')
    image_node = nodes.new('ShaderNodeTexImage')
    image_node.image = img
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    mix = nodes.new('ShaderNodeMixShader')
    links = mat.node_tree.links
    links.new(image_node.outputs['Color'], emission.inputs['Color'])
    links.new(image_node.outputs['Alpha'], mix.inputs[0])
    links.new(transparent.outputs['BSDF'], mix.inputs[1])
    links.new(emission.outputs['Emission'], mix.inputs[2])
    links.new(mix.outputs[0], out.inputs['Surface'])
    if hasattr(mat, 'surface_render_method'):
        mat.surface_render_method = 'DITHERED'
    elif hasattr(mat, 'blend_method'):
        mat.blend_method = 'BLEND'
    mat.use_backface_culling = False
    return mat

P = 0.009   # 1 SVG source unit in Blender
layers = MANIFEST['layer_order']
for i, name in enumerate(layers):
    pivot = MANIFEST['pivots_svg_viewbox'].get(name, [120, 115])
    px, py = ((pivot[0] - 120) * P, (115 - pivot[1]) * P)
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(px, py, 0))
    ctrl = bpy.context.object
    ctrl.name = 'CTRL_' + name
    ctrl.parent = root
    ctrl.location = (px, py, 0)

    bpy.ops.mesh.primitive_plane_add(size=2)
    plane = bpy.context.object
    plane.name = 'ART_' + name
    plane.parent = ctrl
    plane.location = (-px, -py, 0.008 * i)
    plane.scale = (1.08, 1.035, 1)  # viewbox 240x230 * P / 2; plane default size 2
    plane.data.materials.append(image_material(RIG / 'png' / (name + '.png'), name))

# Reusable controller keys for a blocked (NOT final animated) NIM appearance.
# Animator replaces these with hand-directed acting, expressions and audio sync.
for frame, position, scale in [(1,(-2.0,-1.0,0),.0),(48,(-2.0,-1.0,0),.0),
                              (60,(-1.6,-.65,0),.85),(114,(-1.2,-.55,0),.92),
                              (115,(-1.2,-.55,0),.0),(240,(1.2,-.9,0),.0),
                              (260,(1.2,-.75,0),.88),(324,(1.2,-.75,0),.95),
                              (325,(0,0,0),0)]:
    root.location = position
    root.scale = (scale, scale, scale)
    root.keyframe_insert('location', frame=frame)
    root.keyframe_insert('scale', frame=frame)

# A few transform controllers show where deliberate poses belong.
for controller, frames in {
    'CTRL_03_arm_left':[(60,-.1),(78,.25),(104,0)],
    'CTRL_04_arm_right':[(60,.1),(78,-.20),(104,0)],
    'CTRL_10_antenna':[(60,.02),(72,-.15),(98,.0)]
}.items():
    obj = bpy.data.objects.get(controller)
    for frame, radians in frames:
        obj.rotation_euler[2] = radians
        obj.keyframe_insert('rotation_euler', frame=frame)

outdir = ROOT / 'blender'
outdir.mkdir(exist_ok=True)
outpath = outdir / 'GymNotFound_S01E01_STARTER.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(outpath))
print('CREATED', outpath)
print('NOTE: this is only a layered NIM / timeline starter, not a finished film.')
