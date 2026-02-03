###########################################
# Charge field Charge Recycling. Blender python. Multi-particle systems (ps's). 
# Blender version 4.4.3
###########################################
# The project's organization, original particle system (ps), physics forces, 
# handlers, etc. began as a ChatGPT suggested Tornado charge field animation, 
# TornadoAndDebris.py. That script worked fine. I realised tornadoes are too large 
# and complicated for a simple single ps Blender c.f. model. I decided it would be 
# a better ps learning opportunity to try forking that script into this multiple, 
# ps's described by the following. 
###########################################
# The Proton Charge Recycling model begins with a volume of space containing  
# a spinning proton and Charge field charge which passes through space as well
# as the proton, in a well defined manner, as this model attempts to portray.

# A right (red) or left (blue) spinning proton is positioned at (0,0,0). 
# A series of Blender particle systems (ps's) will be added to mimic the 
# proton's local recycling charge field: 

# ps1.ps2. TopVortex, BottomVortex: Hemispheric ps emitters with vortex and 
# turbulence physics create charge intake vorticies into the proton's top 
# and bottom poles.  Ready for particle property refinments.   

# ps3.ps4. TopEM, BottomEM: The proton's north and south hemispheric charge  
# emissions traveling radially outward. Mostly from near the high angular 
# momentum equator. Also ready for refinments.

# The next two may be ps5.ps6. N, S : The surrounding North and South Charge 
# field, charge from all directions, (mostly Top or Bottom), headed for the proton.  

# Once ps1 and 2 streams are established, one can see a direct pole-to-pole, pass-
# through current, charge passing through the proton without any collisions. 

# Charge photons spin and travel at light speed, and can only interact via 
# collisions; lots of collisions, including head-to-head and shoulder to shoulder. 
# Unfortunately, as far as I know, Blender's physics field particles are instances 
# that cannot collide. Some imagination or additional ps's may be needed.   

###########################################
# CURRENT STATUS. 27 Jan 26.


    # Need to automate the emission's charge color. 
    # spin_dir is available and with: 
    #    if spin_dir = -1, then L, if spin_dir = 1, then R,
      
    #coll_name = Top_VORTEX_Assets, spin_dir = -1, L charge, hemi-o down. Want L charge
    #coll_name = Bottom_VORTEX_Assets, spin_dir = 1, R charge, hemi-o up. Want R charge
    #coll_name = Top_EM_Assets, spin_dir = 1, R charge, hemi-o down. Want R charge
    #coll_name = Bottom_EM_Assets, spin_dir = -1, L charge, hemi-o up. Want L charge
    
    # Testing the values of each field's spin_dir, to properly color each ps, R or L used next. 
    # z_sign corresponds to the hemi-sphere equator opening toward +/-Z. 
###########################################
# Controls are at the top. Some Instructions are at the bottom. 
# The script creates objects and registers a frame-change handler. 
#
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

CHARGE_PARTICLE_COUNT = 250   # number of charge particles
CHARGE_LIFETIME = 400         # particle lifetime in frames
#CHARGE_SPEED = 1.8           # initial outward speed for charge
SIMULATION_START_FRAME = 1
SIMULATION_END_FRAME = 360

# Name prefixes (so repeated runs are easier to clean)
TV_ANCHOR = "TopVortexAnchor"
BV_ANCHOR = "BottomVortexAnchor"
TE_ANCHOR = "TopEmAnchor"
BE_ANCHOR = "BottomEmAnchor"

TV_EMITTER = "TopVortexEmitter"   
BV_EMITTER = "BottomVortexEmitter"       
TE_EMITTER = "TopEmEmitter"
BE_EMITTER = "BottomEmEmitter"

TV_CHARGE = "TopVortex_charge_mesh"
BV_CHARGE = "BottomVortex_charge_mesh"
TE_CHARGE = "TopEM_charge_mesh"
BE_CHARGE = "BottomEM_charge_mesh"
       
TV_ASSETS = "Top_VORTEX_Assets"
BV_ASSETS = "Bottom_VORTEX_Assets"
TE_ASSETS = "Top_EM_Assets"
BE_ASSETS = "Bottom_EM_Assets"

TV_FIELDS = "Top_VORTEX_Field"
BV_FIELDS = "Bottom_VORTEX_Field"
TE_FIELDS = "Top_EM_Field"
BE_FIELDS = "Bottom_EM_Field"

TV_HANDLER = "Top_Vortex_handler" 
BV_HANDLER = "Bottom_Vortex_handler"  

EMITTERS = [
    dict(name="TopVortex",      z_sign=+1, mode="vortex", hemi_radius=BASE_RADIUS*5,  spin=-1), 
    dict(name="BottomVortex",   z_sign=-1, mode="vortex", hemi_radius=BASE_RADIUS*5,  spin=+1),
    dict(name="TopEm",          z_sign=+1, mode="emit", hemi_radius=BASE_RADIUS,  spin=1),
    dict(name="BottomEm",       z_sign=-1, mode="emit", hemi_radius=BASE_RADIUS,  spin=-1),
]

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

def clear_previous():     #ps.name =  BottomVortexChargeSettings are not removed
    """Remove objects created by previous runs of this script to avoid duplicates."""
    objs = [o for o in bpy.data.objects if (o.name == TV_ANCHOR or o.name == BV_ANCHOR
        or o.name == TE_ANCHOR or o.name == BE_ANCHOR or o.name == TCF_ANCHOR or o.name == BCF_ANCHOR)]
    # The below print outputs indicates extra TopVortex_mesh and BottomVortex_mesh meshes?
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

def linear_interp(a, b, t):  # Was used with ring placement
    return a + (b - a) * t

def remove_all_objects():
    print("--- Removing all objects ---")
    for _obj in list(bpy.data.objects):
        bpy.data.objects.remove(_obj, do_unlink=True)

def remove_all_collections():
    print("--- Removing all collections ---")
    _scene_col = bpy.context.scene.collection
    for _col in list(bpy.data.collections):
        if _col != _scene_col:
            bpy.data.collections.remove(_col)

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
# HDRI Functions
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

    #bpy.ops.object.modifier_add(type='COLLISION')  # Seems to work fine here
    # if true, the proton emissions cannot escape the proton

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
    #add_continuous_rotation(proton, axis_index=2, speed=0.25, spin_dir=spin_dir)      # axial spin
    add_continuous_rotation(porbit_empty, axis_index=2, speed=0.125, spin_dir=spin_dir)  # orbital spin

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
    bpy.context.scene.frame_end = 360

    if spin_dir=="L": 
        driver.expression = f" -1 * {speed} * {var.name}"   
    else:
        driver.expression = f"{speed} * {var.name}"      
    return

# -----------------------------
# Create anchor 
# -----------------------------
# Latest: Later. Replace name branching with **anchor role**:
def create_charge_anchor(name = "TopVortex", z_sign=1, mode='vortex', hemi_radius=BASE_RADIUS*5):

    ANCHOR_TYPES = {
        ("vortex", +1): TV_ANCHOR,
        ("vortex", -1): BV_ANCHOR,
        ("emit",   +1): TE_ANCHOR,
        ("emit",   -1): BE_ANCHOR,

    }
       
    ANCHOR_Z_OFFSETS = {
        "vortex": 30.0,
        "emit": 0.0,
        "field": 0.0,
    }

    anchor = None

    # Given ANCHOR_TYPES, the 6 if branches are replaced by:
    anchor = bpy.data.objects.new(ANCHOR_TYPES[(mode, z_sign)], None)    
            
    if anchor is None:
        raise RuntimeError(f"No anchor created for mode={mode}, z_sign={z_sign}") 
    # Works good
     
    anchor.empty_display_type = 'SPHERE'  
    anchor.empty_display_size = 0.5
    anchor.location.z = z_sign * ANCHOR_Z_OFFSETS[mode]
    
    bpy.context.collection.objects.link(anchor)   

    return anchor


# -----------------------------
# Create a hemi_emitter   # Working
# -----------------------------
# Refactoring, offloaded the create hemi part of create_hemisphere() to a 
# new function, make_hemi_emitter(). create_hemisphere() needs a new name.
def make_hemi_emitter(anchor, name, z_sign, mode, hemi_radius, 
    hemi_segments, hemi_rings, vortex_strength,  spin_dir):
    ''' Geometry role, shared by all emitters. Hemisphere mesh, Anchor parenting '''
    
    EMITTER_TYPES = {
        ("vortex", +1): TV_EMITTER,
        ("vortex", -1): BV_EMITTER,
        ("emit",   +1): TE_EMITTER,
        ("emit",   -1): BE_EMITTER,
    }

    # Builds hemi-emitter geometry
    mesh = bpy.data.meshes.new(name + "_emitter_mesh")   

    verts = []
    faces = []
    
    # build hemisphere vertices (lat 0..pi/2, lon 0..2pi)
    for i in range(hemi_rings + 1):
        v = i / float(hemi_rings)  # 0..1
        theta = (math.pi / 2.0) * v  # 0..pi/2
        #z = hemi_radius * math.cos(theta)
        #Hemisphere geometry (flip Z)   ##### CHECK #####
        z = z_sign * hemi_radius * math.cos(theta)  
              
        ring_radius = hemi_radius * math.sin(theta)   
        for j in range(hemi_segments):
            phi = (2.0 * math.pi * j) / hemi_segments
            x = ring_radius * math.cos(phi)
            y = ring_radius * math.sin(phi)
            verts.append((x, y, z))
    # faces (quads mostly)
    def idx(r, c):
        return r * hemi_segments + (c % hemi_segments)        
            
    for r in range(hemi_rings):
        for c in range(hemi_segments):
            v0 = idx(r, c)
            v1 = idx(r, c + 1)
            v2 = idx(r + 1, c + 1)
            v3 = idx(r + 1, c)
            faces.append((v0, v1, v2, v3))
    
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    emitter = bpy.data.objects.new(EMITTER_TYPES[(mode, z_sign)], mesh) 
    emitter.location = (0.0, 0.0, 0.0)       
    bpy.context.collection.objects.link(emitter)
    emitter.parent = anchor  
    return emitter


# -----------------------------
# Adding turbulence and vortex fields. # Do Not Use, Not built yet, Function not ready 
# -----------------------------
def turbulence_and_vortex(tv_obj, mode, z_sign):  
    #coll_name = "Bottom_Pole_Fields"    
    coll_name = FIELD_TYPES[(mode, z_sign)]
            
    if coll_name not in bpy.data.collections:
        assets_coll = bpy.data.collections.new(coll_name)
        bpy.context.scene.collection.children.link(assets_coll)
    else:
        assets_coll = bpy.data.collections[coll_name]
        bpy.context.scene.collection.children.link(assets_coll)   

    bpy.ops.object.effector_add(type='TURBULENCE', location=(0.0, 0.0, BOTTOM_VORTEX_HEIGHT * 0.45)) 
    turb_obj = bpy.context.active_object            
    #turb_obj.name = "BottomVortexTurbulence"  
    if turb_obj:
        turb_obj.name = "BottomPoleTurbulence" 
        if hasattr(turb_obj, "field") and turb_obj.field is not None:
            turb_obj.field.strength = 1.0
            turb_obj.field.size = 0.6
            turb_obj.field.flow = 1.0
        turb_obj.parent = anchor  

    #coll.objects.link(obj)
    obj = turb_obj
    move_to_collection(obj, coll_name)              

    bpy.ops.object.effector_add(type='VORTEX', location=(0.0, 0.0, z_sign*VORTEX_HEIGHT * 0.5))  
    vortex_obj = bpy.context.active_object
    if vortex_obj:
        vortex_obj.name = "BottomPoleVortex"
        if hasattr(vortex_obj, "field") and vortex_obj.field is not None:          
            #vortex_obj.field.strength = 7.0  
            vortex_obj.field.strength = spin_dir * vortex_strength            
            vortex_obj.field.distance_max = BASE_RADIUS * 1.1 
                        
            try:
                vortex_obj.field.falloff_type = 'SPHERE'
            except Exception:
                pass
        vortex_obj.parent = anchor

    obj = vortex_obj
    move_to_collection(obj, coll_name)      
    
    bvsettings.effector_weights.vortex = 1.0
    bvsettings.effector_weights.turbulence = 1.0
    bvsettings.effector_weights.gravity = -1.0  
    bvsettings.effector_weights.collection = bpy.data.collections[coll_name]
    
    return emitter


    '''
    # -----------------------------
    # hemisphere Particle System       # Under Consideration/Construction
    # ----------------------------- 
    def create_p_s(anchor, name, z_sign, mode, hemi_radius, hemi_segments, hemi_rings, vortex_strength,  spin_dir) 
        charge_mesh = bpy.data.meshes.new(CHARGE_MESH_TYPES[(mode, z_sign)])
        s = 0.25
        dverts = [(-s,-s,-s),( s,-s,-s),( s, s,-s),(-s, s,-s),( -s,-s,s),( s,-s,s),( s, s,s),(-s, s,s)]
        dfaces = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
        charge_mesh.from_pydata(dverts, [], dfaces)
        charge_mesh.update()       
        
        #### Abvoe, with EMITTER_TYPES[(mode, z_sign)] and CHARGE_MESH_TYPES[(mode, z_sign)]
        # there is a single through line with no if branches. The first branching 
        # occurs here.

        if mode == "emit" and z_sign == 1:

            if spin_dir == 1.0:   # R or L spinning charge colorz, no actual spins yet
                r_charge_obj = bpy.data.objects.new(name, charge_mesh)
                r_charge_obj.data.materials.append(mats["RSpin"]) 
            else:
                l_charge_obj = bpy.data.objects.new(name, charge_mesh)
                l_charge_obj.data.materials.append(mats["LSpin"])         
      
            coll_name = ASSET_TYPES[(mode, z_sign)] 
            #print(f'coll_name = {coll_name}, spin_dir = {spin_dir}')               
            #coll_name = "Top_EM_Assets" 

            if coll_name not in bpy.data.collections:
                assets_coll = bpy.data.collections.new(coll_name)
                bpy.context.scene.collection.children.link(assets_coll)
            else:
                assets_coll = bpy.data.collections[coll_name]
                #bpy.context.scene.collection.children.link(assets_coll)         
            
            # unlink from current collection(s) and link to the hidden assets collection
            #for c in list(cube_obj.users_collection):
            for c in list(r_charge_obj.users_collection):
                #c.objects.unlink(cube_obj)
                c.objects.unlink(r_charge_obj)   

            assets_coll.objects.link(r_charge_obj)
            assets_coll.hide_viewport = True    #  Dimmed in the Outliner
            assets_coll.hide_render = True    #  Dimmed in the Outliner  
            #assets_coll.hide_viewport = False   
            #assets_coll.hide_render = False
            
            return assets_coll           

    '''


# -----------------------------
# Charge emitter (hemisphere)
# -----------------------------
"""Create a hemisphere, emitter, particle system, etc (top or bottom UV sphere half) and particle system."""
def create_hemisphere(anchor, name, z_sign, mode, hemi_radius, 
    hemi_segments=24, hemi_rings=12, vortex_strength=7.0,  spin_dir=1): 
    
    CHARGE_MESH_TYPES = {
        ("vortex", +1): TV_CHARGE,
        ("vortex", -1): BV_CHARGE,
        ("emit",   +1): TE_CHARGE,
        ("emit",   -1): BE_CHARGE,
    }
   
    ASSET_TYPES = {
        ("vortex", +1): TV_ASSETS,
        ("vortex", -1): BV_ASSETS,
        ("emit",   +1): TE_ASSETS,
        ("emit",   -1): BE_ASSETS,
    }
    
    FIELD_TYPES = {
        ("vortex", +1): TV_FIELDS,
        ("vortex", -1): BV_FIELDS,
        ("emit",   +1): TE_FIELDS,
        ("emit",   -1): BE_FIELDS,
    }
    
    
    
    # Make the hemisphere emitter  Good.
    emitter = make_hemi_emitter(anchor, name, z_sign, mode, hemi_radius, 
        hemi_segments=24, hemi_rings=12, vortex_strength=7.0,  spin_dir=1)
   
    #------------------------------
    #* Creates PS
    #------------------------------

    ''' '''
   
    # create_p_s(anchor, name, z_sign, mode, hemi_radius, hemi_segments, hemi_rings, vortex_strength,  spin_dir) 
    
    #assets_coll = create_p_s(anchor, name, z_sign, mode, hemi_radius, 
    #    hemi_segments=24, hemi_rings=12, vortex_strength=7.0,  spin_dir=1)  
    
    charge_mesh = bpy.data.meshes.new(CHARGE_MESH_TYPES[(mode, z_sign)])
    s = 0.25
    dverts = [(-s,-s,-s),( s,-s,-s),( s, s,-s),(-s, s,-s),( -s,-s,s),( s,-s,s),( s, s,s),(-s, s,s)]
    dfaces = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    charge_mesh.from_pydata(dverts, [], dfaces)
    charge_mesh.update()       
    
    #### Abvoe, with EMITTER_TYPES[(mode, z_sign)] and CHARGE_MESH_TYPES[(mode, z_sign)]
    # there is a single through line with no if branches. The first branching 
    # occurs here.

    if mode == "emit" and z_sign == 1:  

        if spin_dir == 1.0:   # R or L spinning charge colorz, no actual spins yet
            r_charge_obj = bpy.data.objects.new(name, charge_mesh)
            r_charge_obj.data.materials.append(mats["RSpin"]) 
        else:
            l_charge_obj = bpy.data.objects.new(name, charge_mesh)
            l_charge_obj.data.materials.append(mats["LSpin"])         
  
        coll_name = ASSET_TYPES[(mode, z_sign)] 
        #print(f'coll_name = {coll_name}, spin_dir = {spin_dir}')               
        #coll_name = "Top_EM_Assets" 

        if coll_name not in bpy.data.collections:
            assets_coll = bpy.data.collections.new(coll_name)
            bpy.context.scene.collection.children.link(assets_coll)
        else:
            assets_coll = bpy.data.collections[coll_name]
            #bpy.context.scene.collection.children.link(assets_coll)         
        
        # unlink from current collection(s) and link to the hidden assets collection
        #for c in list(cube_obj.users_collection):
        for c in list(r_charge_obj.users_collection):
            #c.objects.unlink(cube_obj)
            c.objects.unlink(r_charge_obj)   

        assets_coll.objects.link(r_charge_obj)
        assets_coll.hide_viewport = True    #  Dimmed in the Outliner
        assets_coll.hide_render = True    #  Dimmed in the Outliner  
        #assets_coll.hide_viewport = False   
        #assets_coll.hide_render = False     

        ''' '''
        
        # add particle system to emitter
        teps = emitter.modifiers.new(name="TopEMChargePS", type='PARTICLE_SYSTEM').particle_system     
        tesettings = bpy.data.particles.new(name="TopEMChargeSettings")

        teps.settings = tesettings
        tesettings.particle_size = 1.0
        tesettings.count = CHARGE_PARTICLE_COUNT   
        tesettings.frame_start = SIMULATION_START_FRAME

        tesettings.frame_end = SIMULATION_END_FRAME 
        tesettings.lifetime = CHARGE_LIFETIME  
        tesettings.emit_from = 'FACE'   # faces of the hemisphere surface
        tesettings.physics_type = 'NEWTON'
        tesettings.use_rotations = True
        tesettings.render_type = 'OBJECT'  
        
        tesettings.instance_object = r_charge_obj
        
        # initial velocity outward from hemisphere normals
        tesettings.normal_factor = -1.0   # outward  #0.2  #########
        tesettings.factor_random = 0.3   #0.8   
        tesettings.tangent_factor = 0.2   # equatorial spread 
        #tesettings.effector_weights.gravity = 1.0  # allow some gravity pull ## Only diff    
        tesettings.use_emit_random = True
        tesettings.use_die_on_collision = False   # True ??       
        
        # Add a new collection in which to add Top_pole only Turbulence and 
        # Vortex fields. Thereby separating top and bottom ps field effects. 
        #coll_name = "Top_EM_Field"
        coll_name = FIELD_TYPES[(mode, z_sign)]       
        if coll_name not in bpy.data.collections:
            assets_coll = bpy.data.collections.new(coll_name)
            bpy.context.scene.collection.children.link(assets_coll)
        else:
            assets_coll = bpy.data.collections[coll_name]
            bpy.context.scene.collection.children.link(assets_coll)

        bpy.ops.object.effector_add(type='FORCE', location=(0.0, 0.0, 0.0)) 
        tem_obj = bpy.context.active_object  
        
        #obj = tem_obj    
        #move_to_collection(obj, coll_name) 
        #move_to_collection(obj, "Top_EM_Fields") 
        move_to_collection(tem_obj, coll_name)         
               
        tesettings.effector_weights.vortex = 1.0
        tesettings.effector_weights.turbulence = 1.0
        tesettings.effector_weights.gravity = 0.0
        tesettings.effector_weights.collection = bpy.data.collections[coll_name]
    
    if mode == "emit" and z_sign == -1: 
        #l_charge_obj = bpy.data.objects.new("BottomEM_Obj", charge_mesh)
        #l_charge_obj.data.materials.append(mats["LSpin"]) 

        if spin_dir == 1.0:         
            r_charge_obj = bpy.data.objects.new(name, charge_mesh)
            r_charge_obj.data.materials.append(mats["RSpin"]) 
        else:
            l_charge_obj = bpy.data.objects.new(name, charge_mesh)
            l_charge_obj.data.materials.append(mats["LSpin"])    
               
        #coll_name = "Bottom_EM_Assets"
        coll_name = ASSET_TYPES[(mode, z_sign)]    
        #print(f'coll_name = {coll_name}, spin_dir = {spin_dir}')           
        # Below
        #coll_name = "Bottom_EM_Fields"        

        if coll_name not in bpy.data.collections:
            assets_coll = bpy.data.collections.new(coll_name)
            bpy.context.scene.collection.children.link(assets_coll)
        else:
            assets_coll = bpy.data.collections[coll_name]
            #bpy.context.scene.collection.children.link(assets_coll)         

        for c in list(l_charge_obj.users_collection):
            #c.objects.unlink(cube_obj)
            c.objects.unlink(l_charge_obj)   

        assets_coll.objects.link(l_charge_obj)
        assets_coll.hide_viewport = True    #  Dimmed in the Outliner
        assets_coll.hide_render = True    #  Dimmed in the Outliner  
        #assets_coll.hide_viewport = False   
        #assets_coll.hide_render = False   
        
        # add particle system to emitter
        beps = emitter.modifiers.new(name="BottomEMChargePS", type='PARTICLE_SYSTEM').particle_system     
        besettings = bpy.data.particles.new(name="BottomEMChargeSettings")

        beps.settings = besettings
        besettings.particle_size = 1.0
        besettings.count = CHARGE_PARTICLE_COUNT    # Make Top or Bottom counts
        besettings.frame_start = SIMULATION_START_FRAME

        besettings.frame_end = SIMULATION_END_FRAME 
        besettings.lifetime = CHARGE_LIFETIME  
        besettings.emit_from = 'FACE'   # faces of the hemisphere surface
        besettings.physics_type = 'NEWTON'
        besettings.use_rotations = True
        besettings.render_type = 'OBJECT' 
        
        besettings.instance_object = l_charge_obj 
        
        # initial velocity outward from hemisphere normals
        besettings.normal_factor = 1.0   # outward  #0.2
        besettings.factor_random = 0.3   #0.8   
        besettings.tangent_factor = 0.2   # equatorial spread 
        #tesettings.effector_weights.gravity = 1.0  # allow some gravity pull ## Only diff    
        besettings.use_emit_random = True
        besettings.use_die_on_collision = False   # True ??       
        
        # Add a new collection in which to add Top_pole only Turbulence and 
        # Vortex fields. Thereby separating top and bottom ps field effects. 
        #coll_name = "Bottom_EM_Field"
        coll_name = FIELD_TYPES[(mode, z_sign)]          
           
        if coll_name not in bpy.data.collections:
            assets_coll = bpy.data.collections.new(coll_name)
            bpy.context.scene.collection.children.link(assets_coll)
        else:
            assets_coll = bpy.data.collections[coll_name]
            bpy.context.scene.collection.children.link(assets_coll)

        bpy.ops.object.effector_add(type='FORCE', location=(0.0, 0.0, 0.0)) 
        bem_obj = bpy.context.active_object  
        
        #obj = turb_obj    
        #move_to_collection(obj, coll_name) 
        #move_to_collection(obj, "Top_Pole_Fields") 
        move_to_collection(bem_obj, coll_name)         

        besettings.effector_weights.vortex = 1.0
        besettings.effector_weights.turbulence = 1.0
        besettings.effector_weights.gravity = 0.0
        besettings.effector_weights.collection = bpy.data.collections[coll_name]
    
    if mode == "vortex" and z_sign == 1.0:  
        #if name == "TopVortex":    
        #l_charge_obj = bpy.data.objects.new("TopVortex_Obj", charge_mesh)
        #l_charge_obj.data.materials.append(mats["LSpin"])
        
        if spin_dir == 1.0:         
            r_charge_obj = bpy.data.objects.new(name, charge_mesh)
            r_charge_obj.data.materials.append(mats["RSpin"]) 
        else:
            l_charge_obj = bpy.data.objects.new(name, charge_mesh)
            l_charge_obj.data.materials.append(mats["LSpin"])    
        
        #coll_name = "Top_Vortex_Assets" 
        coll_name = ASSET_TYPES[(mode, z_sign)] 
        #print(f'coll_name = {coll_name}, spin_dir = {spin_dir}')               
        # Below
        #coll_name = "Top_Vortex_Fields"

        if coll_name not in bpy.data.collections:
            assets_coll = bpy.data.collections.new(coll_name)
            bpy.context.scene.collection.children.link(assets_coll)
        else:
            assets_coll = bpy.data.collections[coll_name]
            #bpy.context.scene.collection.children.link(assets_coll)         
        
        # unlink from current collection(s) and link to the hidden assets collection
        #for c in list(cube_obj.users_collection):
        for c in list(l_charge_obj.users_collection):
            #c.objects.unlink(cube_obj)
            c.objects.unlink(l_charge_obj)

        assets_coll.objects.link(l_charge_obj)
        assets_coll.hide_viewport = True    #  Dimmed in the Outliner
        assets_coll.hide_render = True    #  Dimmed in the Outliner        
          
        # add particle system to emitter
        tvps = emitter.modifiers.new(name="TopVortexChargePS", type='PARTICLE_SYSTEM').particle_system   
  
        tvsettings = bpy.data.particles.new(name="TopVortexChargeSettings")
         
        tvps.settings = tvsettings
        #tvsettings.particle_size = 0.5
        tvsettings.particle_size = 1.0
        tvsettings.count = CHARGE_PARTICLE_COUNT    # Make Top or Bottom counts
        tvsettings.frame_start = SIMULATION_START_FRAME
        #tvsettings.frame_end = SIMULATION_START_FRAME + 50  
        tvsettings.frame_end = SIMULATION_END_FRAME 
        tvsettings.lifetime = CHARGE_LIFETIME  
        tvsettings.emit_from = 'FACE'   # faces of the hemisphere surface
        tvsettings.physics_type = 'NEWTON'
        tvsettings.use_rotations = True
        tvsettings.render_type = 'OBJECT'
        
        tvsettings.instance_object = l_charge_obj  
              
        # initial velocity outward from hemisphere normals
        tvsettings.normal_factor = 0.2
        tvsettings.factor_random = 0.8
        tvsettings.tangent_factor = 0.0   
        #tvsettings.effector_weights.gravity = 1.0  # allow some gravity pull ## Only diff    
        tvsettings.use_emit_random = True
        #tvsettings.use_die_on_collision = True
        tvsettings.use_die_on_collision = False

        # ChatGPT wrote. #* Strip vortex logic out of `create_hemisphere()` *without deleting it*
        #* Just move it behind `if mode == "vortex"`
        ############Building a function to be used by both TopVortex and BottomVortex
        # I may be wrong, but I expect tp follow up with a call to a new function for both TV and BV types
        #if mode == "vortex": 
        #   tv_obj = bpy.context.active_object
        #   turbulence_and_vortex(tv_obj, mode, z_sign)  # Maybe just passing tv_obj works  
        #def turbulence_and_vortex(mode, z_sign):    
        if mode == "vortex":  
            v_obj = bpy.context.active_object      
            #tv_obj = bpy.context.active_object
            #def turbulence_and_vortex(mode, z_sign, tv_obj):
            coll_name = FIELD_TYPES[(mode, z_sign)]      
            if coll_name not in bpy.data.collections:
                assets_coll = bpy.data.collections.new(coll_name)
                bpy.context.scene.collection.children.link(assets_coll)
            else:
                assets_coll = bpy.data.collections[coll_name]
                #bpy.context.scene.collection.children.link(assets_coll)          
            # Now the collection needs to be populated
               
            bpy.ops.object.effector_add(type='TURBULENCE', location=(0.0, 0.0, TOP_VORTEX_HEIGHT * 0.45)) 
            turb_obj = bpy.context.active_object        
            if turb_obj:
                turb_obj.name = "TopPoleTurbulence"
                if hasattr(turb_obj, "field") and turb_obj.field is not None:
                    turb_obj.field.strength = 1.0
                    turb_obj.field.size = 0.6
                    turb_obj.field.flow = 1.0
                turb_obj.parent = anchor

            move_to_collection(turb_obj, coll_name) 
            
            bpy.ops.object.effector_add(type='VORTEX', location=(0.0, 0.0, z_sign*VORTEX_HEIGHT * 0.5))  
            #vortex_obj = bpy.ops.object.effector_add(type='VORTEX', location=(0.0, 0.0, z_sign*VORTEX_HEIGHT * 0.5))  
            vortex_obj = bpy.context.active_object
            if vortex_obj:
                vortex_obj.name = "TopPoleVortex"
                if hasattr(vortex_obj, "field") and vortex_obj.field is not None:          

                    #vortex_obj.field.strength = 7.0  
                    vortex_obj.field.strength = spin_dir * vortex_strength            
                    #vortex_obj.field.distance_max = BASE_RADIUS * 2.5   #??
                    #vortex_obj.field.distance_max = BASE_RADIUS * 10               
                    #vortex_obj.field.distance_max = BASE_RADIUS    
                    vortex_obj.field.distance_max = BASE_RADIUS * 1.1     
                    try:
                        vortex_obj.field.falloff_type = 'SPHERE'
                    except Exception:
                        pass
                vortex_obj.parent = anchor
                move_to_collection(vortex_obj, coll_name)    

            tvsettings.effector_weights.vortex = 1.0
            tvsettings.effector_weights.turbulence = 1.0
            tvsettings.effector_weights.gravity = 1.0
            tvsettings.effector_weights.collection = bpy.data.collections[coll_name]
                   
    elif mode == "vortex" and z_sign == -1.0:  
        
        if spin_dir == 1.0:         
            #r_charge_obj = bpy.data.objects.new("BottomVortex_mesh", charge_mesh)
            r_charge_obj = bpy.data.objects.new(name, charge_mesh)
            r_charge_obj.data.materials.append(mats["RSpin"]) 
        else:
            #l_charge_obj = bpy.data.objects.new("BottomVortex_mesh", charge_mesh)
            l_charge_obj = bpy.data.objects.new(name, charge_mesh)
            l_charge_obj.data.materials.append(mats["LSpin"])    
    
        # Put the charge_obj into a "Bottom_Vortex_Fields" collection that is 
        # hidden in viewport/render 
           
        #coll_name = "Bottom_Vortex_Assets"
        coll_name = ASSET_TYPES[(mode, z_sign)]
        #print(f'coll_name = {coll_name}, spin_dir = {spin_dir}') 
        #print(f'coll_name = {name + "_Obj"}, spin_dir = {spin_dir}')  
                
        if coll_name not in bpy.data.collections:
            assets_coll = bpy.data.collections.new(coll_name)
            bpy.context.scene.collection.children.link(assets_coll)
        else:
            assets_coll = bpy.data.collections[coll_name]

        # unlink from current collection(s) and link to the hidden assets collection
        for c in list(r_charge_obj.users_collection):
            c.objects.unlink(r_charge_obj)

        assets_coll.objects.link(r_charge_obj)
        assets_coll.hide_viewport = True   #  Dimmed in the Outliner
        assets_coll.hide_render = True    #  Dimmed in the Outliner

        bvps = emitter.modifiers.new(name="BottomVortexChargePS", type='PARTICLE_SYSTEM').particle_system
        bvsettings = bpy.data.particles.new(name="BottomVortexChargeSettings") 
        bvps.settings = bvsettings
        
        #bvsettings.particle_size = 0.5   
        bvsettings.particle_size = 1.0       
        bvsettings.count = CHARGE_PARTICLE_COUNT
        bvsettings.frame_start = SIMULATION_START_FRAME
        bvsettings.frame_end = SIMULATION_END_FRAME 
        bvsettings.lifetime = CHARGE_LIFETIME  
        bvsettings.emit_from = 'FACE'   # faces of the hemisphere surface
        bvsettings.physics_type = 'NEWTON'
        bvsettings.use_rotations = True
        bvsettings.render_type = 'OBJECT'
        bvsettings.instance_object = r_charge_obj
        # Where is the initial velocity outward from hemisphere normals?
        bvsettings.normal_factor = 0.2
        bvsettings.factor_random = 0.8
        bvsettings.tangent_factor = 0.0    
        bvsettings.use_emit_random = True
        #bvsettings.use_die_on_collision = True
        bvsettings.use_die_on_collision = False

        #def turbulence_and_vortex(mode, z_sign):
        #def turbulence_and_vortex(mode, z_sign):    
        if mode == "vortex": 
            v_obj = bpy.context.active_object     
            #turb_obj = bpy.context.active_object              
            #coll_name = "Bottom_Pole_Fields"    
            coll_name = FIELD_TYPES[(mode, z_sign)]
                    
            if coll_name not in bpy.data.collections:
                assets_coll = bpy.data.collections.new(coll_name)
                bpy.context.scene.collection.children.link(assets_coll)
            else:
                assets_coll = bpy.data.collections[coll_name]
                bpy.context.scene.collection.children.link(assets_coll)   

            bpy.ops.object.effector_add(type='TURBULENCE', location=(0.0, 0.0, BOTTOM_VORTEX_HEIGHT * 0.45)) 
            turb_obj = bpy.context.active_object            
            #turb_obj.name = "BottomVortexTurbulence"  
            if turb_obj:
                turb_obj.name = "BottomPoleTurbulence" 
                if hasattr(turb_obj, "field") and turb_obj.field is not None:
                    turb_obj.field.strength = 1.0
                    turb_obj.field.size = 0.6
                    turb_obj.field.flow = 1.0
                turb_obj.parent = anchor  

            #coll.objects.link(obj)
            obj = turb_obj
            move_to_collection(obj, coll_name)              

            bpy.ops.object.effector_add(type='VORTEX', location=(0.0, 0.0, z_sign*VORTEX_HEIGHT * 0.5))  
            vortex_obj = bpy.context.active_object
            if vortex_obj:
                vortex_obj.name = "BottomPoleVortex"
                if hasattr(vortex_obj, "field") and vortex_obj.field is not None:          
                    #vortex_obj.field.strength = 7.0  
                    vortex_obj.field.strength = spin_dir * vortex_strength            
                    vortex_obj.field.distance_max = BASE_RADIUS * 1.1 
                                
                    try:
                        vortex_obj.field.falloff_type = 'SPHERE'
                    except Exception:
                        pass
                vortex_obj.parent = anchor

            obj = vortex_obj
            move_to_collection(obj, coll_name)      
            
            bvsettings.effector_weights.vortex = 1.0
            bvsettings.effector_weights.turbulence = 1.0
            bvsettings.effector_weights.gravity = -1.0  # allow some gravity pull    
            
            bvsettings.effector_weights.collection = bpy.data.collections[coll_name]

    return emitter

# -----------------------------
# Animation handler
# -----------------------------
def vortex_frame_handler(scene, name):
    #ChatGPT wrote. In the future
    #python
    #def frame_handler(scene, cfg):
    
    frame = scene.frame_current

    if name == "TopVortex":
        # global oscillating "charge strength" (simulating proton wind variation)
        charge_osc = 1.0 + CHARGE_AMPLITUDE * math.sin(frame * CHARGE_FREQ)  # Emissions in z plane
        #charge_osc = 0.5 + CHARGE_AMPLITUDE * math.sin(frame * CHARGE_FREQ)
        #charge_osc = 2 + CHARGE_AMPLITUDE * math.sin(frame * CHARGE_FREQ)            
        # find anchor
        anchor = bpy.data.objects.get(TV_ANCHOR)
        if not anchor:
            return
        # Optionally vary vortex strength object fields if present (for charge)
        v = bpy.data.objects.get("TopChargeVortex")
        if v and hasattr(v, "field") and v.field is not None:
            # make vortex field strength depend on charge_osc (and optionally ring tightening)
            try:  # Several lines added varying the initial .strength value.       
                #v.field.strength = 12.5 * (0.6 + 0.8 * (charge_osc - 0.5))   # Blooms out like a trumpet     
                #v.field.strength = 10.0 * (0.6 + 0.8 * (charge_osc - 0.5))   # 2 much rotation, almost a vortex column. Could be longer?   
                v.field.strength = 5.0 * (0.6 + 0.8 * (charge_osc - 0.5))   # Good
                #v.field.strength = 1.0 * (0.6 + 0.8 * (charge_osc - 0.5))   # Slow rot
                # The first number in the v.field.strength appears to determine the orbital rate of the particles about the z-axis
                # optionally adjust distance or other params:  
                #v.field.distance_max = BASE_RADIUS * (1.5 + 0.5 * (charge_osc - 1.0)) # Emissions in z plane  
                #print('v.field.distance_max = ',v.field.distance_max)
            except Exception as e:
                # if the field API differs we just skip setting it rather than crash
                #print("Could not update TopChargeVortex.field:", e)
                pass
                
        #This will safely update vortex strength each frame and will not cause the handler to 
        #throw if the vortex object is missing.  
        #tv = bpy.data.objects.get("TopVortex") 
        #print("TopVortex = ", tv)   
          
    elif name == "BottomVortex":
        # global oscillating "charge strength" (simulating proton wind variation)
        charge_osc = 1.0 + CHARGE_AMPLITUDE * math.sin(frame * CHARGE_FREQ)  # Emissions in z plane
        #charge_osc = 0.5 + CHARGE_AMPLITUDE * math.sin(frame * CHARGE_FREQ)
        #charge_osc = 2 + CHARGE_AMPLITUDE * math.sin(frame * CHARGE_FREQ)            
        # find anchor
        anchor = bpy.data.objects.get(BV_ANCHOR)
        if not anchor:
            return
        # Optionally vary vortex strength object fields if present (for charge)
        v = bpy.data.objects.get("BottomChargeVortex")
         
        if v and hasattr(v, "field") and v.field is not None:
            # make vortex field strength depend on charge_osc (and optionally ring tightening)
            try:  # Several lines added varying the initial .strength value.       
                v.field.strength = 5.0 * (0.6 + 0.8 * (charge_osc - 0.5))   # Good   

                #bpy.context.object.show_instancer_for_render = False    # Nope
                #bpy.context.object.show_instancer_for_viewport = False                 
                             
            except Exception as e:
                # if the field API differs we just skip setting it rather than crash
                print("Could not update BottomChargeVortex.field:", e)
                        
# -----------------------------
# Helper to register the handler
# -----------------------------

def register_handler(name):
    # ChatGPT wrote.  Move handler registration to a **single loop**
    # Make `field` and `emit` modes *data-only* (no handlers)
    # If there is no time-domain signal → **no handler**. 

    # remove existing handler if present
    handlers = bpy.app.handlers.frame_change_pre
    for h in list(handlers):
        #if getattr(h, "__name__", "") == HANDLER:    ##### Original #######
        if getattr(h, "__name__", "") == TV_HANDLER: 
            try:
                handlers.remove(h)
            except Exception:
                pass                 
        elif getattr(h, "__name__", "") == BV_HANDLER:   
            try:
                handlers.remove(h)
            except Exception:
                pass  

    # set up a small wrapper function with stable name so we can remove it later
    def vortex_charge_handler(scene, name):
        vortex_frame_handler(scene, name)

    # name it for easier removal
    if name == "TopVortex":
        vortex_charge_handler.__name__ = TV_HANDLER
 
    elif name == "BottomVortex":
        vortex_charge_handler.__name__ = BV_HANDLER
        
    bpy.app.handlers.frame_change_pre.append(vortex_charge_handler)    
    #print('vortex_charge_handler = ', vortex_charge_handler.__name__) 

def remove_handler():
    handlers = bpy.app.handlers.frame_change_pre
    for h in list(handlers):
        #if getattr(h, "__name__", "") == HANDLER:     ##### Original #######
        # Convert handler removal to suffix-based:
        if h.__name__.endswith("_handler"):
            try:
                handlers.remove(h)
            except Exception:
                pass

# -----------------------------
# main setup
# -----------------------------

def build_emitter_from_config(config):
    # This function 1. Removes a handler, 2. creates an emitter and at the same time 
    # 3. creates an anchor, then 4. registers the handle. For all six emitters. The only 
    # thing it hasen't done is 5. Sets the Scene parameters, which is likely better done 
    # in vortex_frame_handler(scene, name). 
    
    remove_handler()  # optional: or move to a higher-level call

    emitter = create_hemisphere(
        anchor=create_charge_anchor(
            config["name"],
            config["z_sign"],
            config["mode"],
            config["hemi_radius"]
        ),
        name=config["name"],
        z_sign=config["z_sign"],
        mode=config["mode"],
        hemi_radius=config["hemi_radius"],
        spin_dir=config.get("spin", 1),
    )
    # Registering is done as soon as the emitter is created(?)
    register_handler(config["name"])
    return emitter


def remove_charge_groups(): 
    remove_handler()
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
               
    # ideally clear extra data-blocks too (materials, meshes) if desired
    #print("Top Charge vortex removed.")  # Top_VortexTurbulence and TopChargeVortex empties remain
    # See 

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

#create_proton(loc_x=0, loc_y=0, loc_z=0, type='BL', spin_mat=spin_mat_l)

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
    
    for cfg in EMITTERS:  # This builds every emitter in EMITTERS[], each anchor, mesh and charge instance
        build_emitter_from_config(cfg)

# After the script has completed a full run, hide the vortex emitters with these console commands
# bpy.data.objects["TopVortexEmitter"].show_instancer_for_viewport = False 
# bpy.data.objects["BottomVortexEmitter"].show_instancer_for_viewport = False 