#######################################
# Charge field Charge Recycling. Blender python. Multi-particle systems (ps's). 
# Blender version 4.4.3
###########################################
# The project's organization, original particle system (ps), physics forces, 
# handlers, etc. began as a ChatGPT suggested Tornado charge field animation, 
# TornadoAndDebris.py. That script worked fine. I realised tornadoes are too  
# large and complicated for a simple single ps Blender c.f. model. I decided 
# it would be a better ps learning opportunity to try forking that script  
# into this multiple ps's project described by the following. 
###########################################
# The Proton Charge Recycling model begins with a volume of space containing  
# a spinning proton and Charge field charge which passes through space as well
# as the proton, in a well defined manner, as this model attempts to portray.

# A right (red) or left (blue) spinning proton is positioned at (0,0,0). 
# A series of Blender particle systems (ps's) will be added to mimic the 
# proton's local recycling charge field: 

# ps1.ps2: TopVortex, BottomVortex: Hemispheric ps emitters with vortex and 
# turbulence physics create charge intake vorticies into the proton's top 
# and bottom poles. Ready for particle property settings adjustments/refinments.   

# ps3.ps4: The proton's north and south hemispheric charge  
# emissions traveling radially outward. Mostly from near the high angular 
# momentum equator. Right spinning charge mainly enters the proton's bottom 
# pole and is emitted from the proton's top hemisphere, while left spinning 
# anti-charge generally enters the proton's top pole is redirected by internal 
# charge recycling particle collisions to emit from the proton's bottom hemisphere. 

# Charge photons spin and travel at light speed, and can only interact via 
# collisions; lots of collisions, including head-to-head and side-by-side.
# Increasing a photon's charge energy beyond lightspeed doubles the photon 
# charge's radius, up to the size of electrons, neutrons and protons. Most 
# charge is too small to see at this scale, exagerated for the model's sake. 
# Reasoning only larger charge is shown. It can be easily changed.

# Blender's physics field particles are instances that cannot collide. Some 
# imagination is required.   

# I'm hoping I can next assume the proton's spin direction and velocity is 
# determined by the ratio of the charge/anti-charge it receives.

###########################################
# Controls are at the top. Some Instructions are at the bottom. 
# The script creates objects and registers a frame-change handler. 
# To remove the animation and objects later, call remove_charge_groups() 
# at the bottom of this script or restart Blender.   

import bpy
import math
import random
from mathutils import Vector, Euler
import mathutils
import pathlib
import datetime

# -----------------------------
# USER PARAMETERS (tweak here)
# -----------------------------
P_RADIUS = 5                # proton radius
VORTEX_HEIGHT = 8.0   
TOP_VORTEX_HEIGHT = 8.0       # total height (Blender units)
BOTTOM_VORTEX_HEIGHT = -8.0   # total height (Blender units)
BASE_RADIUS = 0.8*P_RADIUS    # P_RADIUS is 5, the smallest emitter is slightly smaller

CHARGE_AMPLITUDE = 0.9        # how strongly charge field ups the spin (multiplier)
CHARGE_FREQ = 0.02            # oscillation frequency of charge strength (per frame)

#CHARGE_PARTICLE_COUNT = 650   # number of charge particles
CHARGE_PARTICLE_COUNT = 5000   # number of charge particles
#CHARGE_LIFETIME = 190         # particle lifetime in frames
CHARGE_LIFETIME = 225         # particle lifetime in frames
#CHARGE_LIFETIME = LOOP         # particle lifetime in frames

#CHARGE_SPEED = 1.8           # initial outward speed for charge
SIMULATION_START_FRAME = 1
SIMULATION_END_FRAME = 1000  

# Name prefixes (so repeated runs are easier to clean)
TE_ANCHOR = "TopEmAnchor"
BE_ANCHOR = "BottomEmAnchor"
TV_ANCHOR = "TopVortexAnchor"
BV_ANCHOR = "BottomVortexAnchor"

TE_EMITTER = "TopEmEmitter"
BE_EMITTER = "BottomEmEmitter"
TV_EMITTER = "TopVortexEmitter"   
BV_EMITTER = "BottomVortexEmitter"       

TE_CHARGE = "TopEM_charge_mesh"
BE_CHARGE = "BottomEM_charge_mesh"
TV_CHARGE = "TopVortex_charge_mesh"
BV_CHARGE = "BottomVortex_charge_mesh"

TE_ASSET = "Top_EM_Assets"
BE_ASSET = "Bottom_EM_Assets"       
TV_ASSET = "Top_VORTEX_Assets"
BV_ASSET = "Bottom_VORTEX_Assets"

TE_FIELD = "Top_EM_Field"
BE_FIELD = "Bottom_EM_Field"
TV_FIELD = "Top_VORTEX_Field"
BV_FIELD = "Bottom_VORTEX_Field"
   
TE_PS_TYPE = "TopEMChargePS"
BE_PS_TYPE = "BottomEMChargePS" 
TV_PS_TYPE = "TopVortexChargePS"
BV_PS_TYPE = "BottomVortexChargePS"     
              
TE_PS_SETTING = "TopEMChargeSettings"
BE_PS_SETTING = "BottomEMChargeSettings" 
TV_PS_SETTING = "TopVortexChargeSettings"
BV_PS_SETTING = "BottomVortexChargeSettings"

TV_HANDLER = "Top_Vortex_handler" 
BV_HANDLER = "Bottom_Vortex_handler"  


SYSTEMS = {            
    ("emit", +1): {
        "anchor": TE_ANCHOR,
        "emitter": TE_EMITTER,
        "charge_mesh": TE_CHARGE,
        "asset": TE_ASSET,
        "field": TE_FIELD,
        "ps_settings": TE_PS_SETTING,
        "ps_type": TE_PS_TYPE,
        "z_offset": 0.0
    },
    
    ("emit", -1): {
        "anchor": BE_ANCHOR,
        "emitter": BE_EMITTER,
        "charge_mesh": BE_CHARGE,
        "asset": BE_ASSET,
        "field": BE_FIELD,
        "ps_settings": BE_PS_SETTING,
        "ps_type": BE_PS_TYPE,
        "z_offset": 0.0
    },
    
    ("vortex", +1): {
        "anchor": TV_ANCHOR,
        "emitter": TV_EMITTER,
        "charge_mesh": TV_CHARGE,
        "asset": TV_ASSET,
        "field": TV_FIELD,
        "ps_settings": TV_PS_SETTING,
        "ps_type": TV_PS_TYPE,
        "z_offset": 30.0
    },
    
    ("vortex", -1): {
        "anchor": BV_ANCHOR,
        "emitter": BV_EMITTER,
        "charge_mesh": BV_CHARGE,
        "asset": BV_ASSET,
        "field": BV_FIELD,
        "ps_settings": BV_PS_SETTING,
        "ps_type": BV_PS_TYPE,
        "z_offset": 30.0
    }
}

VORTEX_CFG = {
    +1: dict(turb_z=TOP_VORTEX_HEIGHT * 0.45, name_prefix="Top"),
    -1: dict(turb_z=BOTTOM_VORTEX_HEIGHT * 0.45, name_prefix="Bottom")
}

EMITTERS = [
    dict(name="TopEm", z_sign=+1, mode="emit", hemi_radius=BASE_RADIUS,  spin=1),
    dict(name="BottomEm", z_sign=-1, mode="emit", hemi_radius=BASE_RADIUS,  spin=-1),
    dict(name="TopVortex", z_sign=+1, mode="vortex", hemi_radius=BASE_RADIUS*5,  spin=-1), 
    dict(name="BottomVortex", z_sign=-1, mode="vortex", hemi_radius=BASE_RADIUS*5,  spin=+1),
]

# -----------------------------
# Charge Flow Controller
# -----------------------------
class ChargeFlowController:

    def __init__(self):
        self.top_emit = None
        self.bottom_emit = None
        self.top_vortex = None
        self.bottom_vortex = None

    def find_systems(self):  

        self.top_emit = bpy.data.particles.get("TopEMChargeSettings")
        self.bottom_emit = bpy.data.particles.get("BottomEMChargeSettings")
        
        self.top_vortex = bpy.data.objects.get("TopPoleVortex")
        self.bottom_vortex = bpy.data.objects.get("BottomPoleVortex")
                        
    def update(self, frame):

        # oscillating charge environment   # Orig
        charge_wave = 1.0 + CHARGE_AMPLITUDE * math.sin(frame * CHARGE_FREQ)  # Orig

        spin_bias = 0.15
        
        # vortex intake strength
        if self.top_vortex and self.top_vortex.field:   # Orig 
            self.top_vortex.field.strength = -5.0 * (charge_wave + spin_bias)   # Orig Changed sign

        if self.bottom_vortex and self.bottom_vortex.field:   # Orig 
            self.bottom_vortex.field.strength = 5.0 * (charge_wave - spin_bias)   # Orig Changed sign

FLOW = ChargeFlowController()

# -----------------------------
# Proton spin materials
# -----------------------------  
spin_mat_r = bpy.data.materials.new('RSpin')
spin_mat_l = bpy.data.materials.new('LSpin')
emission_mat = bpy.data.materials.new('Emission')
def ensure_materials():
    mats = {}
    def make(name, color):
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name)
        mat.diffuse_color = color
        mats[name] = mat
    make("RSpin", (1, 0, 0, 1))
    make("LSpin", (0, 0, 1, 1))
    make("Emission", (1, 1, 1, 1))
    return mats
mats = ensure_materials()

# -----------------------------
# utility functions
# -----------------------------
def move_to_collection(obj, coll_name):
    coll = bpy.data.collections.get(coll_name)
    if not coll:
        coll = bpy.data.collections.new(coll_name)
        bpy.context.scene.collection.children.link(coll)

    # unlink from all current collections
    for c in obj.users_collection:
        c.objects.unlink(obj)
    coll.objects.link(obj)
    return

def remove_all_collections():
    print("--- Removing all collections ---")
    _scene_col = bpy.context.scene.collection
    for _col in list(bpy.data.collections):
        if _col != _scene_col:
            bpy.data.collections.remove(_col)

def clear_previous():  
    """Remove objects created by previous runs of this script to avoid duplicates."""
    # The outputs are intended for user convenience
    objs = [o for o in bpy.data.objects if (o.name == TV_ANCHOR or o.name == BV_ANCHOR
        or o.name == TE_ANCHOR or o.name == BE_ANCHOR )]
    # The below print outputs are intended for user convenience
    for o in objs:
        print('o.name = ', o.name, ' removed and unlinked')        
        bpy.data.objects.remove(o, do_unlink=True)
    # also remove particle systems data-blocks if present
    for ps in list(bpy.data.particles):
        # ps.name =  BottomVortexChargeSettings are not yet removed
        print('ps.name = ', ps.name)        
        if (ps.name.startswith("TopVortex") or (ps.name.startswith("BottomVortex"))):
            print('ps.name = ', ps.name, ' removed')   
            bpy.data.particles.remove(ps)
    # remove meshes named by script
    for m in list(bpy.data.meshes):
        print('m.name = ', m.name) 
        if (m.name.startswith("TopVortex") or (m.name.startswith("BottomVortex"))):        
            print('m.name = ', m.name, ' removed')   
            bpy.data.meshes.remove(m)


def remove_all_objects():
    print("--- Removing all objects ---")
    for _obj in list(bpy.data.objects):
        bpy.data.objects.remove(_obj, do_unlink=True)


def purge_orphans():
    print("--- Purging orphaned datablocks (Outliner) ---")
    try:
        bpy.ops.outliner.orphans_purge(
            do_local_ids=True,
            do_linked_ids=False,
            do_recursive=True
        )
    except RuntimeError:
        pass

def remove_charge_groups(): 
    remove_handler()  # Use only manually
    clear_previous()
    remove_all_objects()
    remove_all_collections()
    purge_orphans()  
    # The hdri flat western plain remains.
    # remove any created particle instance object
    ob = bpy.data.objects.get("TopVortex_Obj")
    if ob:
        bpy.data.objects.remove(ob, do_unlink=True)
   
    ob = bpy.data.objects.get("BottomVortex_Obj")
    if ob:
        bpy.data.objects.remove(ob, do_unlink=True)
        
    ob = bpy.data.objects.get("TopEm_Obj")
    if ob:
        bpy.data.objects.remove(ob, do_unlink=True) 
        
    ob = bpy.data.objects.get("BottomEm_Obj")
    if ob:
        bpy.data.objects.remove(ob, do_unlink=True) 
    
# -----------------------------
# Create lights and camera  
# -----------------------------

def two_lights(origin=(0,0,0)):
    #import mathutils
    #bpy.ops.object.select_all(action='DESELECT')       
    positions = [
        (origin[0]+65, origin[1]-65, origin[2]+65), 
        (origin[0]-65, origin[1]-65, origin[2]+65)]      
    for pos in positions:
        bpy.ops.object.light_add(type='AREA', location=pos)
        light = bpy.context.object
        light.data.size = 40
        light.data.energy = 40000
        # Point the light at the origin
        direction = mathutils.Vector((origin[0], origin[1], origin[2])) - mathutils.Vector(pos)
        light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    return

def setup_camera(loc, rot):  
    # Add a camera. At a location and orientation. 
    """
    Create and setup the camera. 
    """
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    camera = bpy.context.active_object
    return camera
    
# -----------------------------
# HDRI Functions. hdri's provide their own lighting
# -----------------------------
# How to apply HDRIs with a Blender Python script.  	
#	https://www.youtube.com/watch?v=xz9Tn6rUzzg 
# The following script creates and renders images including HDRI backgrounds. 
# Creating and connecting Blender Shader editor nodes, creating and rendering 
# each unique hdri file in an hdri folder, outputting to a separate render folder. 
def apply_hdri(path_to_image ):
    #import pathlib
    world_node_tree = bpy.context.scene.world.node_tree
    world_node_tree.nodes.clear()

    location_x = 0

    image_obj = bpy.data.images.load(path_to_image)

    environment_texture_node = world_node_tree.nodes.new(type='ShaderNodeTexEnvironment')
    environment_texture_node.image = image_obj
    location_x += 300  # To spread out the shader nodes horizontally

    background_node = world_node_tree.nodes.new(type="ShaderNodeBackground")
    background_node.inputs["Strength"].default_value = 1.0
    background_node.location.x = location_x
    location_x += 300
    
    world_output_node = world_node_tree.nodes.new(type="ShaderNodeOutputWorld")
    world_output_node.location.x = location_x

    from_node = environment_texture_node
    to_node = background_node
    world_node_tree.links.new(from_node.outputs["Color"], to_node.inputs["Color"])

    from_node = background_node
    to_node = world_output_node
    world_node_tree.links.new(from_node.outputs["Background"], to_node.inputs["Surface"])

def render_image():
    output_folder_path = pathlib.Path.home()/'renders'
    time_stamp = datetime.datetime.now().strftime("%H-%M-%S")
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = str(output_folder_path/f"img_{time_stamp}.png")
    bpy.ops.render.render(write_still=True)

# The main() for HDRI Functions
def mainHDRI():  
    hadris_folder = pathlib.Path.home()/"hdris"
    for image_path in hadris_folder.iterdir():
        apply_hdri(str(image_path))
        render_image()   

# -----------------------------
# Create the charge recycling Proton
# -----------------------------
def add_proton_grp(loc_x, loc_y, loc_z, type = 'L', spin_mat = spin_mat_l):
    spin_dir = "L" if spin_mat == spin_mat_l else "R"
    collection_name = f"{type}Proton_Collection"
    My_collection = bpy.data.collections.new(collection_name)    
    bpy.context.scene.collection.children.link(My_collection)

    # Step 1: Create orbit empty at origin
    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=0.15, location=(loc_x, loc_y, loc_z))
    porbit_empty = bpy.context.active_object
    porbit_empty.name = f"{type}Proton_spin"   # maybe change from _orbit to _spin    

    # Step 2: Create proton at offset relative to empty
    #bpy.ops.mesh.primitive_uv_sphere_add(radius=P_RADIUS, location=(loc_x + P_RADIUS, loc_y, loc_z))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=P_RADIUS, location=(loc_x, loc_y, loc_z))
    proton = bpy.context.active_object
    proton.name = f"{type}proton"
    proton.data.name = f"{type}proton"
    #proton.data.materials.append(spin_mat)
    proton.data.materials.append(mats["LSpin" if spin_dir == "L" else "RSpin"])    
    bpy.ops.object.shade_smooth()

    # Step 3: Parent proton to empty BEFORE any animation drivers
    proton.parent = porbit_empty

    # Step 4: Add the torus spin markers
    bpy.context.view_layer.objects.active = proton
    dimx = {'axis': 'x', 'dim': 0}
    dimy = {'axis': 'y', 'dim': 1}
    dimz = {'axis': 'z', 'dim': 2}
    for dime in (dimx, dimy, dimz):
        bpy.ops.mesh.primitive_torus_add(
            major_radius=P_RADIUS, minor_radius=P_RADIUS / 15, location=proton.location)
        ring = bpy.context.active_object
        ring.rotation_euler[dime['dim']] = math.pi / 2
        ring.data.materials.append(emission_mat)
        bpy.ops.object.shade_smooth() 
        bpy.context.view_layer.objects.active = proton
        proton.select_set(True)
        bpy.ops.object.join()

    # Step 5: Add drivers
    add_continuous_rotation(porbit_empty, axis_index=2, speed=0.125, spin_dir=spin_dir)  
    My_collection.objects.link(porbit_empty)
    My_collection.objects.link(proton)
    return porbit_empty, proton


def add_continuous_rotation(obj, axis_index=2, speed=-0.05, spin_dir="L"):
    driver = obj.driver_add("rotation_euler", axis_index).driver
    var = driver.variables.new()
    var.name = "frame_number"
    var.type = "SINGLE_PROP"
    target = var.targets[0]
    target.id_type = 'SCENE'
    target.id = bpy.context.scene
    target.data_path = "frame_current"

    bpy.context.scene.frame_end = SIMULATION_END_FRAME 

    if spin_dir=="L": 
        driver.expression = f" -1 * {speed} * {var.name}"   
    else:
        driver.expression = f"{speed} * {var.name}"      
    return

# -----------------------------
# Create anchor 
# -----------------------------
def create_charge_anchor(config):
    z_sign=config["z_sign"]
    mode=config["mode"] 
    cfg = SYSTEMS[(mode, z_sign)]     
    
    anchor = None
    #anchor = bpy.data.objects.new(ANCHOR_TYPES[(mode, z_sign)], None)     
    anchor = bpy.data.objects.new(cfg["anchor"], None)   
     
    if anchor is None:
        raise RuntimeError(f"No anchor created for mode={mode}, z_sign={z_sign}")      
    anchor.empty_display_type = 'SPHERE'  
    anchor.empty_display_size = 0.5
    #anchor.location.z = z_sign * ANCHOR_Z_OFFSETS[mode]   
    anchor.location.z = z_sign * cfg["z_offset"] 
     
    bpy.context.collection.objects.link(anchor)   
    return anchor

# -----------------------------
# Create a hemi_emitter (with profile)
# -----------------------------
def make_profiled_hemi_emitter(
    anchor,
    config,
    hemi_segments,
    hemi_profile,   # density profile list
):

    name=config["name"]
    z_sign=config["z_sign"]
    mode=config["mode"]
    hemi_radius=config["hemi_radius"]
    #spin=config["spin"]  
    #Then access it like:
    cfg = SYSTEMS[(mode, z_sign)]

    mesh = bpy.data.meshes.new(name + "_emitter_mesh")

    verts = []
    faces = []

    total_subrings = sum(hemi_profile)   # e.g. 114
    band_count = len(hemi_profile)       # e.g. 9
    band_angle = (math.pi / 2) / band_count   # 90° / bands

    ring_index = 0

    # -------- build vertices --------
    for band_i, subrings in enumerate(hemi_profile):

        theta_start = band_i * band_angle
        theta_end   = (band_i + 1) * band_angle

        for s in range(subrings):
            t = s / subrings
            theta = theta_start + (theta_end - theta_start) * t

            z = z_sign * hemi_radius * math.cos(theta)
            ring_radius = hemi_radius * math.sin(theta)

            for j in range(hemi_segments):
                phi = (2.0 * math.pi * j) / hemi_segments
                x = ring_radius * math.cos(phi)
                y = ring_radius * math.sin(phi)
                verts.append((x, y, z))

            ring_index += 1

    rings = ring_index  # total rings

    # -------- faces --------
    def idx(r, c):
        return r * hemi_segments + (c % hemi_segments)

    for r in range(rings - 1):
        for c in range(hemi_segments):
            v0 = idx(r, c)
            v1 = idx(r, c + 1)
            v2 = idx(r + 1, c + 1)
            v3 = idx(r + 1, c)
            faces.append((v0, v1, v2, v3))

    mesh.from_pydata(verts, [], faces)
    mesh.update()
    emitter = bpy.data.objects.new(cfg["emitter"], mesh)
    emitter.location = (0.0, 0.0, 0.0)
    bpy.context.collection.objects.link(emitter)
    emitter.parent = anchor

    return emitter

# -----------------------------
# Charge emitter (hemisphere)
# -----------------------------
"""Create a hemisphere, emitter, particle system, etc (top or bottom UV sphere half) and particle system."""
def create_hemisphere(anchor, config, hemi_segments=24, hemi_rings=12, vortex_strength=7.0): 
    name=config["name"]
    z_sign=config["z_sign"]
    mode=config["mode"]
    #hemi_radius=config["hemi_radius"]
    spin=config["spin"]
    cfg = SYSTEMS[(mode, z_sign)]

    def create_charge_mesh(anchor, config): 
        #charge_mesh = bpy.data.meshes.new(CHARGE_MESH_TYPES[(mode, z_sign)]) 
        charge_mesh = bpy.data.meshes.new(cfg["charge_mesh"])
        s = 0.25
        dverts = [(-s,-s,-s),(s,-s,-s),(s,s,-s),(-s,s,-s),(-s,-s,s),(s,-s,s),(s,s,s),(-s,s,s)]
        dfaces = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
        charge_mesh.from_pydata(dverts, [], dfaces)
        charge_mesh.update() 
        return charge_mesh 

    def assign_charge_spin_color(anchor, config):
        if spin == 1.0:   
            charge_obj = bpy.data.objects.new(name, charge_mesh)
            charge_obj.data.materials.append(mats["RSpin"]) 
        else:
            charge_obj = bpy.data.objects.new(name, charge_mesh)
            charge_obj.data.materials.append(mats["LSpin"])         
        return charge_obj
    
    # On the ToDo list, not yet used, generate the profile dynamically:
    def lat_profile_from_spin(spin_rate, bands=9):
        # spin_rate: 0..1 normalized
        profile = []
        for i in range(bands):
            lat = i / (bands-1) * 90  # degrees
            peak = 35 + spin_rate * 10  # In future, peak shifts with spin
            density = math.exp(-((lat - peak)**2)/(2*(12**2)))
            rings = int(1 + density * 30)
            profile.append(rings)
        print(f'profile = {profile}')
        return profile
    ''' 
    hemi_profile = lat_profile_from_spin(spin_rate=0.6)
    # Currently outputs four identical profiles
    profile = [1, 2, 10, 25, 29, 14, 3, 1, 1]
    ''' 
        
    def charge_collection(coll_name):
        if coll_name not in bpy.data.collections:
            assets_coll = bpy.data.collections.new(coll_name)
            bpy.context.scene.collection.children.link(assets_coll)
        else:
            assets_coll = bpy.data.collections[coll_name]
            #bpy.context.scene.collection.children.link(assets_coll)         

        # unlink from current collection(s) and link to the hidden assets collection
        for c in list(charge_obj.users_collection):
            #c.objects.unlink(cube_obj)
            c.objects.unlink(charge_obj)   

        assets_coll.objects.link(charge_obj)
        assets_coll.hide_viewport = True    #  Dimmed in the Outliner
        assets_coll.hide_render = True    #  Dimmed in the Outliner  


    def add_particle_system_to_emitter(config):

        #eps = emitter.modifiers.new(name=PS_TYPES[(mode, z_sign)], type='PARTICLE_SYSTEM').particle_system         
        eps = emitter.modifiers.new(name=cfg["ps_type"], type='PARTICLE_SYSTEM').particle_system         

        #settings = bpy.data.particles.new(name=PS_SETTINGS[(mode, z_sign)])
        settings = bpy.data.particles.new(name=cfg["ps_settings"])
        eps.settings = settings
        #print('settings = ', settings)
           
        # The following are common to all four ps's.        
        settings.particle_size = 1.0
        settings.count = CHARGE_PARTICLE_COUNT  
        
        # 'Burst lifecycle mode'. 1_000 frames makes a good lifecycle
        settings.frame_start = SIMULATION_START_FRAME
        settings.frame_end = SIMULATION_END_FRAME 
        settings.lifetime = CHARGE_LIFETIME 

        settings.emit_from = 'FACE'   # faces of the hemisphere surface
        settings.physics_type = 'NEWTON'   
        
        # magnetic-like flow behavior # Not worked
        #settings.brownian_factor = 0.0
        #settings.damping = 0.04
        
        # Spins the particles R with respect to their forward velocity
        settings.use_rotations = True
        settings.use_dynamic_rotation = True
        settings.angular_velocity_factor = spin * 5.0      
        settings.render_type = 'OBJECT'          
        settings.instance_object = charge_obj
        # initial velocity outward from hemisphere normals
        
        if mode == 'emit': 
            settings.normal_factor = - z_sign * 4
        elif mode == 'vortex':                    
            settings.normal_factor = - z_sign 
              
        settings.factor_random = 0.0   # Maybe vel randomizing, then let = 0.0   
        settings.tangent_factor = 0.0   # equatorial spread 
        #tesettings.effector_weights.gravity = 1.0  # allow some gravity pull ## Only diff    
        settings.use_emit_random = True
        settings.use_die_on_collision = False 
        
        return settings
          
    #------------------------------
    #* Creates the hemisphere emitter
    #------------------------------

    hemi_profile = [0,1,3,20,150,250,150,15,5]   
    
    emitter = make_profiled_hemi_emitter(
        anchor=anchor,
        config=config,
        hemi_segments=24,
        hemi_profile=hemi_profile,
    )  

    #------------------------------
    #* Creates PS
    #------------------------------
    charge_mesh = create_charge_mesh(anchor, config)
        
    charge_obj = assign_charge_spin_color(anchor, config)

    # Put the particle system into its collection.    
    charge_collection(cfg["asset"])

    settings = add_particle_system_to_emitter(config)
    
    #coll_field_name = FIELD_TYPES[(mode, z_sign)] x
    coll_field_name = cfg["field"] 
    
    if coll_field_name not in bpy.data.collections:
        assets_coll = bpy.data.collections.new(coll_field_name)
        bpy.context.scene.collection.children.link(assets_coll)
    else:
        coll_field_name = bpy.data.collections[coll_field_name]
        bpy.context.scene.collection.children.link(coll_field_name)
    
    #------------------------------
    #* The final branching in create_hemisphere() 
    #------------------------------      

    if mode == "emit" :  
               
        bpy.ops.object.effector_add(type='FORCE', location=(0.0, 0.0, 0.0)) 
        
        em_obj = bpy.context.active_object  
        move_to_collection(em_obj, coll_field_name) 
                
        # 'emit' types don't have vortex or turb
        settings.effector_weights.gravity = 0.0
        settings.effector_weights.collection = bpy.data.collections[coll_field_name]

    if mode == "vortex": 
        bpy.ops.object.effector_add(type='TURBULENCE', location=(0.0, 0.0, z_sign * VORTEX_CFG[z_sign]['turb_z'])) 
        #print('Turbulence location = ', z_sign * VORTEX_CFG[z_sign]['turb_z']) # One of either the Turb or Vortex is off
        turb_obj = bpy.context.active_object 
        if turb_obj:
            turb_obj.name = VORTEX_CFG[z_sign]['name_prefix'] + "PoleTurbulence"
            if hasattr(turb_obj, "field") and turb_obj.field is not None:
                turb_obj.field.strength = 1.0
                turb_obj.field.size = 0.6
                turb_obj.field.flow = 1.0
            turb_obj.parent = anchor
        move_to_collection(turb_obj, coll_field_name) 
        
        bpy.ops.object.effector_add(type='VORTEX', location=(0.0, 0.0, z_sign * VORTEX_CFG[z_sign]['turb_z'])) 
        #print('Vortex location = ', z_sign * VORTEX_CFG[z_sign]['turb_z'] ) # One of either the Turb or Vortex is off
        vortex_obj = bpy.context.active_object
        if vortex_obj:
            vortex_obj.name = VORTEX_CFG[z_sign]['name_prefix'] + "PoleVortex"
            if hasattr(vortex_obj, "field") and vortex_obj.field is not None:          
                vortex_obj.field.strength = spin * vortex_strength 
                vortex_obj.field.distance_max = BASE_RADIUS * 1.1     
                try:
                    vortex_obj.field.falloff_type = 'SPHERE'
                except Exception:
                    pass
            vortex_obj.parent = anchor
            move_to_collection(vortex_obj, coll_field_name)    

        #settings.effector_weights.vortex = 1.0
        settings.effector_weights.vortex = 0.5  # Easier to see spiraling V
        settings.effector_weights.turbulence = 1.0
        settings.effector_weights.gravity = z_sign * 1.0
        settings.effector_weights.collection = bpy.data.collections[coll_field_name]

    return emitter

# -----------------------------
# Animation handler
# -----------------------------

def charge_flow_handler(scene):    
    FLOW.update(scene.frame_current) 
          
# -----------------------------
# Helper to register the handler
# -----------------------------

def register_flow_handler():    

    handlers = bpy.app.handlers.frame_change_pre

    for h in list(handlers):
        if getattr(h, "__name__", "") == "charge_flow_handler":
            handlers.remove(h)

    handlers.append(charge_flow_handler)


def remove_handler():
    handlers = bpy.app.handlers.frame_change_pre
    for h in list(handlers):
        #if getattr(h, "__name__", "") == HANDLER:     ##### Original #######
        # Convert handler removal to suffix-based:
        if h.__name__.endswith("_handler"):
            try:
                #print('Remove, h = ', h)
                handlers.remove(h)
                #print('h = ', h)
            except Exception:
                pass

# -----------------------------
# main setup
# -----------------------------

def build_emitter_from_config(config):
    emitter = create_hemisphere(
        anchor=create_charge_anchor(config),
        config=config,
    )
    return emitter


#####################################################
# Manually un-comment individual functions, Then 
# re-comment out that function(s) and move to the next.
######################################################

# 1. Either press "a" and "x", to delete objects, then selecting and 
# deleting collections; then "File" "Clean Up" and "Purge Unused Data"; 
# remove_charge_groups() does all that.

#remove_charge_groups()  #############

# Running remove_charge_groups() and adding a proton at the same time 
# doesn't work - ReferenceError: StructRNA of type Material has been removed

# 2. Add a camera. At a location and orientation. Given "overcast_soil_2_4k.exr" 
# and a good view of the horizon and sky toward -X, I then positioned
# the camera directly across the top_vortex at the origin at +X=100. ...
# Uncomment the three lines and run

#loc = (200, 0, -45)  # Good 
#rot = (1.775, 0, 1.55)
#setup_camera(loc, rot)  #############

# 3. # Add ALL the emitters in EMITTERS[]
#for cfg in EMITTERS:    
#    build_emitter_from_config(cfg)

# 4. The HDRI background image needs to be located in a separate 
# folder, here /Users/ME/hdris also see the # HDRI Functions, line 112 above.
#path_to_image = str(pathlib.Path.home()/"hdris"/"overcast_soil_4k.exr")
#path_to_image = str(pathlib.Path.home()/"hdris"/"overcast_soil_2_4k.exr")
#path_to_image = str(pathlib.Path.home()/"hdris"/"approaching_storm_4k.exr")
#apply_hdri(str(pathlib.Path.home()/"hdris"/"overcast_soil_2_4k.exr"))   ############

# 5. In case lights are needed
#two_lights()

# 6. Add the spinning, charge recycling proton
#loc_x, loc_y, loc_z = 0, 0, 0
#proton = add_proton_grp(loc_x, loc_y, loc_z, type='R', spin_mat=spin_mat_r)   ######### Right spin proton
#proton = add_proton_grp(loc_x, loc_y, loc_z, type='L', spin_mat=spin_mat_l)   ######### Left spin proton   

if __name__ == "__main__":
    
    loc_x, loc_y, loc_z = 0, 0, 0
    proton = add_proton_grp(loc_x, loc_y, loc_z, type='R', spin_mat=spin_mat_r)   ######### Right spin proton
    
    for cfg in EMITTERS:  
        build_emitter_from_config(cfg)

    register_flow_handler()
    
    
'''    
# After the scene has completed a full run, hide the vortex emitters
# and add some randomness with these console commands
bpy.data.particles["TopEMChargeSettings"].distribution = 'RAND'
bpy.data.objects["TopVortexEmitter"].show_instancer_for_viewport = False 
bpy.data.objects["BottomVortexEmitter"].show_instancer_for_viewport = False 
'''