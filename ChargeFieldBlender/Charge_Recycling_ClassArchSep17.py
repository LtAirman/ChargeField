#######################################
# Blender python .py file. Blender version 4.4.3
###########################################
# Charge field Charge Recycling. This Proton Charge Recycling model simulates 
# Miles Mathis' Charge field theory, Charge Recycling (CR) diagram. Showing a 
# spinning proton and its local, recycling charge field. 

# The project's organization, original particle system (ps), physics forces, 
# handlers, etc. began as a ChatGPT suggested Tornado charge field animation, 
# TornadoAndDebris.py. Which worked fine and I shared it. Of course tornadoes
# are just too big and complicated for a simple single ps Blender c.f. model. 
# Decided it would be a better idea to try forking that script into a 'charge
# Charge Recycling model, using four or more ps's, making a series of 
# various changes, mainly ChatGPT suggested that I've tried implementing. The 
# initial CR model could be described as a collection of procedural functions.
 
# More recently, in order to better learn Blender python and improve the 
# project's script and with continued ChatGPT lead, that 'structure' has been 
# migrated to its present, more object oriented class architecture. 

# Eventually it may come together. It continues to be a worthwhile opportunity. 

###########################################
# The vacuum of space is not empty, it is stiff with 'Charge' photons, real 
# (tiny) particles amounting to 19 times as much mass as all 'visible' 
# matter present--protons, neutrons, and electrons. Charge, by virtue of 
# its small size, naturally travels and spins at light speed, with both
# linear and angular momenta. Protons, neutrons, electrons, and the Earth 
# itself consists of and constantly recycle charge in a well defined manner.
 
# Generally, Earth's radialy outward and from our perspective upward, charge 
# emissions, enter a vertical spin axis oriented, left or right spinning 
# proton's bottom pole. That charge is redirected by collisions inside the 
# proton, and will eventually be emitted from the proton's top hemisphere, 
# usually from the spinning proton's faster moving equatorial latitudes. 
# At the same time, left spinning, 'anti-charge' is entering the proton's 
# top pole which is then later emitted from the proton's bottom hemisphere. 
# That's a quick generalized description. Its more correct to say that all 
# atomic matter consists of both matter and anti-matter, protons spinning 
# right or left, which constantly recycle both charge and anti-charge, 
# charge photons moving forward with opposite spins.

# This Proton Charge Recycling model simulates Miles Mathis' Charge Recycling 
# diagram, showing a spinning proton and its recycling charge. Real charge 
# can only interact through real collisions. Real charge collisions include 
# head-to-head and side-by-side. Blender's 'physics particle fields' particle 
# systems (ps) consist of instances, mathematical 'copies' that cannot collide. 
# Some imagination is required.  

# A vertical spin axis oriented proton is positioned at (0,0,0). The proton's 
# near side will be spinning right (red) or left (blue). The model can show
# a non-spinning, close to zero equatorial tangential velocity as white. 

# A series of Blender particle systems (ps's) are added to mimic the proton's 
# local recycling charge field: 

# TopEmission, BottomEmission: The proton's north and south hemispheric charge 
# emissions travel radially outward, mostly from the lower latitudes', highest 
# angular momentum equator while the least amount of emissions occur at the 
# poles. Simulated by 2 hemi-emitters inside the proton. 

# TopVortex, BottomVortex: Hemispheric Blender ps emitters with vortex and 
# turbulence physics above and below the proton poles create charge intake 
# vorticies into the proton poles.

# This 3D simulation lets someone see charge moving forward along its spin 
# axis. I believe that spin orientation results from the photon's foward 
# light speed limit, in a balanced equilibrium with the photon's tangential 
# spin velocity, light speed limit.  

# There's more charge present than has been 'diagrammed' in this CR model  

###########################################
# Status. 17 Sep 26. Implemented the 'Marching Orders' (MO)s, from
# 'YOU ARE HERE' TO 'clean procedural version'; worked perfectly. 
#  All went smoothly. 

# MO: 'FLOW.update() owns the sampling'.
###ME. Completed. `FLOW.update()` is the single place that samples. 

# MO: 'Handler becomes FLOW.update() only'.    
###ME. Done. The entire contents of charge_flow_handler(scene) is  
# FLOW.update(). The current version and bkup are now "known-good". 

# MO: 'Retire find_systems'.  
###ME. The controller's find_systems() and its call in delayed_flow_setup() 
# were removed. Running the script the proton continued to spin properly.

# MO: 'Remove redundant individual handles'. 
###ME. Done. Replaced self.top_emit, self.bottom_emit, self.top_vortex, 
# self.bottom_vortex variables with recommended and more elegant 
# self.fields = particle_fields, with self.fields["TopVortex"].emitter 
# and self.fields["BottomVortex"].emitter. 

# MO: 'clean procedural version'. 
###ME. The procedural functions associated with 
# build_emitter_from_config(config) gone. There are 
# utility/cleanup/scene functs I would not so easily mess with. 
# More likely moving to an Add-on will determine those changes.
# And a goodly number of code notes, especially in migrating to  
# a class architecture that will take me longer to sort through.

###ME. From our last exchange, just before the MOs:
# ChatGPT wrote. You have this:
# 'self.emitter.location = (loc_x, loc_y, loc_z)'
# inside `ParticleField.create_profiled_hemi_emitter()`.
# But those variables don't belong to the method's argument list  
###ME. Agreed.
# ChatGPT cont. I'd eventually expect the location to come from the 
# field's configuration or anchor relationship, rather than from
# mysterious variables floating in the surrounding namespace. 
# But **leave this .alone until the registry/controller cleanup is 
# stable.**
###ME. Everythings gone so smoothly, Thank you. This is the first opportunity 
# I've had to rethink things. 
# To be clear, according to'the c.f. physics', the four CR fields result from 
# the interaction between the proton and larger ambient charge # field present. 
# The 4 fields' anchors should be children of the proton anchor, so that when 
# the proton moves through space, the 4 CR fields move with it.

# Is it possible to tie the 4 fields to a moving proton? I suppose since 
# we're talking about Newtonian animation, as long as it can be formulated 
# its likely possible(?)

# The 4 fields form the pluses and minuses between protons (or rather, 
# electron/proton pairs) that enable atomic bonding. 

# Might we be able to add an electron to the simulation? The electron follows 
# the same general rules as the ptoton. The electron also spins as it moves 
# through space. The electron also forms the same 4 fields of much smaller 
# numbers of the same charge particles. The electron is able to otbit 
# the proton pole, thereby interacting with the proton fields to enhance
# ep_to_ep atomic bonding. 

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
from bpy.app.handlers import persistent

# -----------------------------
# USER PARAMETERS (tweak here)
# -----------------------------
P_RADIUS = 5                   # proton radius
VORTEX_HEIGHT = 8.0   
TOP_VORTEX_HEIGHT = 8.0        # total height (Blender units)
BOTTOM_VORTEX_HEIGHT = -8.0    # total height (Blender units)
BASE_RADIUS = 0.8*P_RADIUS     # P_RADIUS is 5, the smallest emitter is slightly smaller

CHARGE_AMPLITUDE = 0.9         # how strongly charge field ups the spin (multiplier)
CHARGE_FREQ = 0.02             # oscillation frequency of charge strength (per frame)

CHARGE_PARTICLE_COUNT = 5000   # number of charge particles. Looking for the sampling error. 
#CHARGE_LIFETIME = 190         # particle lifetime in frames
CHARGE_LIFETIME = 225
#CHARGE_LIFETIME = LOOP

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

TE_CHARGE = "TopEmChargeMesh"
BE_CHARGE = "BottomEmChargeMesh"
TV_CHARGE = "TopVortexCharge_mesh"
BV_CHARGE = "BottomVortexChargeMesh"

TE_ASSET = "TopEmAssets"
BE_ASSET = "BottomEmAssets"
TV_ASSET = "TopVortexAssets"
BV_ASSET = "BottomVortexAssets"

TE_FIELD = "TopEmField"
BE_FIELD = "BottomEmField"
TV_FIELD = "TopVortexField"
BV_FIELD = "BottomVortexField"
   
TE_PS_TYPE = "TopEMChargePS"
BE_PS_TYPE = "BottomEMChargePS"
TV_PS_TYPE = "TopVortexChargePS"
BV_PS_TYPE = "BottomVortexChargePS"
              
TE_PS_SETTING = "TopEMChargeSettings"
BE_PS_SETTING = "BottomEMChargeSettings"
TV_PS_SETTING = "TopVortexChargeSettings"
BV_PS_SETTING = "BottomVortexChargeSettings"

TV_HANDLER = "TopVortexHandler" 
BV_HANDLER = "BottomVortexHandler"

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

# Right or Left particle system sets build right or left hand rule passing vortices at (0,0,0).
EMITTERS_RIGHT = [   # Rt-hand rule. Charge enters the bottom pole, Anti-Charge enters top. 
    dict(name="TopEm", z_sign=+1, mode="emit", hemi_radius=BASE_RADIUS,  spin=+1),
    dict(name="BottomEm", z_sign=-1, mode="emit", hemi_radius=BASE_RADIUS,  spin=-1),
    dict(name="TopVortex", z_sign=+1, mode="vortex", hemi_radius=BASE_RADIUS*5,  spin=-1), 
    dict(name="BottomVortex", z_sign=-1, mode="vortex", hemi_radius=BASE_RADIUS*5,  spin=+1),
]

EMITTERS_LEFT = [   # Left-hand rule. Anti-Charge enters the bottom pole, Charge enters top 
    dict(name="TopEm", z_sign=+1, mode="emit", hemi_radius=BASE_RADIUS,  spin=-1),
    dict(name="BottomEm", z_sign=-1, mode="emit", hemi_radius=BASE_RADIUS,  spin=+1),
    dict(name="TopVortex", z_sign=+1, mode="vortex", hemi_radius=BASE_RADIUS*5,  spin=+1), 
    dict(name="BottomVortex", z_sign=-1, mode="vortex", hemi_radius=BASE_RADIUS*5,  spin=-1),
]

# -----------------------------
# Charge Flow Controller ChargeFlowController.  -- reads Blender measurements
# -----------------------------
class ChargeFlowController:

    def __init__(self, particle_fields): 
        
        self.fields = particle_fields
        
        # The ChargeFlowController may now be said to own 
        # the four particle_fields["name"]. A milestone goal. 
        
        # The four handles below were replaced with self.fields above & below.
        #self.top_emit = particle_fields["TopEm"]
        #self.bottom_emit = particle_fields["BottomEm"]
        #self.top_vortex = particle_fields["TopVortex"]
        #self.bottom_vortex = particle_fields["BottomVortex"]
                    
    def update(self): # FLOW.update.
        
        STATE.top_intake = self.sample_intake(
            #self.top_vortex.emitter,
            self.fields["TopVortex"].emitter,
            +1
        )

        STATE.bottom_intake = self.sample_intake(
            #self.bottom_vortex.emitter,
            self.fields["BottomVortex"].emitter,
            -1
        )

        STATE.update()
        
        apply_state_to_proton()

        pass

    def sample_intake(self, emitter, z_sign, radius=BASE_RADIUS*1.5, height=2.0): # Smaller sampling volume
        ## As when a changing number of field particles alters the proton spin.
        # Blender has its particular way of doing things.         
        # `obj.evaluated_get(depsgraph)` gets the simulated/emitted particle data for the current frame
        # `eval_obj.particle_systems[0]` reads the evaluated particle system
        # `eval_obj.matrix_world @ p.location` converts particle location into world space
        ### https://docs.blender.org/api/current/bpy.types.Depsgraph.html  
        
        if emitter is None:
            return 0

        depsgraph = bpy.context.evaluated_depsgraph_get()
        eval_obj = emitter.evaluated_get(depsgraph)
    
        psys = eval_obj.particle_systems[0] if eval_obj.particle_systems else None
        
        if not psys: 
            return 0

        count = 0
        z_center = z_sign * P_RADIUS

        for p in psys.particles:
            loc = eval_obj.matrix_world @ p.location

            if abs(loc.z - z_center) < height:
                if (loc.x**2 + loc.y**2) < radius**2:
                    count += 1

        #print('At the end', emitter, 'particles =', len(psys.particles), 'sample =', count)

        return count
    
            
class ProtonState:    # Should be concerned with only the physics 
    def __init__(self):
        # Constant spin works good 

        self.top_intake = 0.0
        self.bottom_intake = 0.0        

        self.spin_signal = 0.0
        self.spin_accel = 0.0        
        self.spin_rate = 0.0

    def update(self):  # ProtonState.update()
        
        # The proton spin direction and velocity will be a function of the top and
        # bottom charge intake ratio/imbalance as in 'imbalance' below, but first,          
        
        # Proton spin test. Sampled top and bottom intake values.
        if self.top_intake == self.bottom_intake:   
            self.top_intake += 1   # So the spin rate doesn't equal zero. Needs work.         
        
        # A time-varying ratio oscillator might may be used as a proxy particle count 
        # generator instead of an actual sample counter. 
        #phase = math.sin(frame * 0.03)
        #self.top_intake = 50 + 40 * max(0, phase)
        #self.bottom_intake = 50 + 40 * max(0, -phase)
        # Results in 5 full cycles: (R,W,B,W, ...) in 1000 frames.     
        # Looking for an excuse.
        
        imbalance = self.top_intake - self.bottom_intake
        total = max(    
            1.0,
            self.top_intake + self.bottom_intake
        )
        #total = 1
        
        self.spin_signal = imbalance / total
        
        gain = 0.0025   # Good clip.
        #gain = 0.1
        #gain = 2  # Might need a gain control
        
        #self.spin_rate = gain * self.spin_signal # Fine constant rate for starters. 
        # For nicer speed-up slow-down motions, and maybe a slightly faster 'constant' rate.
        self.spin_accel = gain * self.spin_signal
        self.spin_rate += self.spin_accel
        self.spin_rate *= 0.99  


STATE = ProtonState()
#print('STATE = ', STATE)
# Outputs:
#STATE =  <__main__.ChargeFlowController.ProtonState object at 0x0000026E72C97E50>
# Along with:
#Info: Deleted 17 data-block(s)
#MAIN finished
#delayed_flow_setup
#flow handler registered
   
   
class ParticleField:    
    # Currently calling the class build() method from 
    # within if __name__ == "__main__". 
    # along with a particle_fields Field handle repository
     
    # Method list
    #1. get_or_create_collection(name)    
    #2. create_anchor(cfg) 
    #3. create_profiled_hemi_emitter(cfg)
    #4. create_charge_mesh(cfg)
    #5. assign_charge_spin_color(cfg)
    #6. add_particle_system_to_emitter(cfg)
    #7. add_force_fields(cfg)  
    #8. build(cfg)  
    
    num_of_fields = 0
    field_names = []
    
    def __init__(self, cfg):  
        
        # These objects are assigned in the methods.
        self.anchor = None   
        self.emitter = None   
        self.charge_mesh = None      
        self.charge_obj = None      
        self.settings = None     
        self.em_object = None    
        self.vortex_object = None   
        self.turbulence_object = None  
        self.coll_name = None
           
        # The variables present in cfg EMITTERS    
        self.name = cfg["name"] 
        self.z_sign = cfg["z_sign"]    
        self.mode = cfg["mode"]
        self.hemi_radius = cfg["hemi_radius"]        
        self.spin = cfg["spin"] 

        # The variables present in SYSTEMS. 
        #    "anchor": BV_ANCHOR,
        #    "emitter": BV_EMITTER,
        #    "charge_mesh": BV_CHARGE,
        #    "asset": BV_ASSET,
        #    "field": BV_FIELD,
        #    "ps_settings": BV_PS_SETTING,
        #    "ps_type": BV_PS_TYPE,
        #    "z_offset": 30.0
        
        ParticleField.num_of_fields += 1       
        ParticleField.field_names.append(self.name)


    def get_or_create_collection(self, name):
        # A Helper function collecting 3 repeat patterns in ParticleField() 

        coll = bpy.data.collections.get(name)

        if coll is None:
            coll = bpy.data.collections.new(name)
            bpy.context.scene.collection.children.link(coll)
        return coll
                
                   
    def create_anchor(self, cfg):  

        self.anchor = bpy.data.objects.new(SYSTEMS[(self.mode, self.z_sign)]['anchor'], None)

        if self.anchor is None:
            raise RuntimeError(f"No anchor created for mode={self.mode}, z_sign={self.z_sign}")
        # Errors if one of the 4 cfg's from EMITTER were missing.
              
        self.anchor.empty_display_type = 'SPHERE'  
        self.anchor.empty_display_size = 0.5
        
        self.anchor.location.z = self.z_sign * SYSTEMS[(self.mode, self.z_sign)]['z_offset']
        bpy.context.collection.objects.link(self.anchor)  # The 4 PF ps anchors are linked
        
        #print(self.__dict__) 
        # Good Output, albeit limited to anchors.

        return self.anchor


    def create_profiled_hemi_emitter(self, cfg):
        
        hemi_profile = [0,1,3,20,150,250,150,15,5] 
        
        hemi_segments=24
        verts = []
        faces = []
        total_subrings = sum(hemi_profile)   # e.g. 114
        band_count = len(hemi_profile)       # e.g. 9
        band_angle = (math.pi / 2) / band_count   # 90° / bands
        ring_index = 0     

        mesh = bpy.data.meshes.new(self.name + "_emitter_mesh")
        
        self.emitter = bpy.data.objects.new(SYSTEMS[(self.mode, self.z_sign)]['emitter'], mesh)

        # -------- build vertices --------
        for band_i, subrings in enumerate(hemi_profile):

            theta_start = band_i * band_angle
            theta_end   = (band_i + 1) * band_angle

            for s in range(subrings):
                t = s / subrings
                theta = theta_start + (theta_end - theta_start) * t

                z = self.z_sign * self.hemi_radius * math.cos(theta)
                ring_radius = self.hemi_radius * math.sin(theta)

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

        # There is also a small code detail I want you to keep an 
        # eye on ...: self.emitter.location = (loc_x, loc_y, loc_z)
        # that's something we'll want to clean up
        ### Affirmative, thank you. This note will do for now.
        self.emitter.location = (loc_x, loc_y, loc_z) ##########  ##########  #########
        
        bpy.context.collection.objects.link(self.emitter)  # The collection's link to the emitter
        self.emitter.parent = self.anchor
        
        #print(self.__dict__) # Good Output. 
        #{'anchor': bpy.data.objects['TopEmAnchor'], 'emitter': bpy.data.objects['TopEmEmitter'], 'settings': None, 'vortex': None, 'turbulence': None, 'name': 'TopEm', 'z_sign': 1, 'mode': 'emit', 'hemi_radius': 4.0, 'spin': -1}
        #{'anchor': bpy.data.objects['BottomEmAnchor'], ...
        # ... 

        return self.emitter


    def create_charge_mesh(self, cfg): 

        self.charge_mesh = bpy.data.meshes.new(SYSTEMS[(self.mode, self.z_sign)]['charge_mesh'])
        s = 0.25
        dverts = [(-s,-s,-s),(s,-s,-s),(s,s,-s),(-s,s,-s),(-s,-s,s),(s,-s,s),(s,s,s),(-s,s,s)]
        dfaces = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
        self.charge_mesh.from_pydata(dverts, [], dfaces)
        self.charge_mesh.update() 
        
        return self.charge_mesh 


    def assign_charge_spin_color(self, cfg):
        
        self.charge_obj = bpy.data.objects.new(self.name + 'ChargeObject', self.charge_mesh)        
        
        if self.spin == 1.0: 
            self.charge_obj.data.materials.append(get_mat("RSpin"))   
        else:
            self.charge_obj.data.materials.append(get_mat("LSpin"))                   
        return self.charge_obj


    def add_particle_system_to_emitter(self, cfg):   
        # Copying the ProceduralFunction form
        
        # Comment. eps is a self.emitter modifier and self.settings is bpy.data
        # Why can both be made equal in the next 3 lines?
        eps = self.emitter.modifiers.new(SYSTEMS[(self.mode, self.z_sign)]["ps_type"], type='PARTICLE_SYSTEM').particle_system 

        self.settings = bpy.data.particles.new(SYSTEMS[(self.mode, self.z_sign)]["ps_settings"])
        
        eps.settings = self.settings
        #print('self.settings = ', self.settings) 
        #print('eps.settings = ', eps.settings)
        #self.settings =  <bpy_struct, ParticleSettings("TopEMChargeSettings") at 0x000001C825635408>
        #eps.settings =  <bpy_struct, ParticleSettings("TopEMChargeSettings") at 0x000001C825635408>
        ###ME. Not ready to delete yet ... a reminder there's plenty to learn.
        
        # The following settings are common to all four ps's.        
        self.settings.particle_size = 1.0
        self.settings.count = CHARGE_PARTICLE_COUNT  

        # 'Burst lifecycle mode'. 1_000 frames makes a good lifecycle
        self.settings.frame_start = SIMULATION_START_FRAME
        self.settings.frame_end = SIMULATION_END_FRAME 
        self.settings.lifetime = CHARGE_LIFETIME 

        self.settings.emit_from = 'FACE'   # faces of the hemisphere emitter's surface
        self.settings.physics_type = 'NEWTON'  
        
        # Spins the particles with respect to their forward velocity
        self.settings.use_rotations = True
        self.settings.use_dynamic_rotation = True
        self.settings.angular_velocity_factor = self.spin * 5.0      
        self.settings.render_type = 'OBJECT'          
        self.settings.instance_object = self.charge_obj  
         
        # Emitter 
        self.settings.factor_random = 0.0   #
        self.settings.tangent_factor = 0.0   # 
        self.settings.use_emit_random = True
        self.settings.use_die_on_collision = False 
        
        # This isolates fields between multiple ParticleField instances.
        self.coll_name = SYSTEMS[(self.mode, self.z_sign)]["asset"]
        
        coll = self.get_or_create_collection(self.coll_name)        

        # Tell the particle settings to only use effectors from this collection
        try:
            self.settings.effector_weights.collection = coll
        except Exception:
            # older/newer API differences: ignore if not available
            pass        

        return self.settings  
    
        
    def  add_force_fields(self, cfg):

        if self.mode == "emit" :  
             
            self.settings.normal_factor = 5.0 * -1 * self.z_sign 
            # Allows the emit particles to properly emerge 'outward' (neg value)             
            self.settings.effector_weights.gravity = 0.0 * self.z_sign
            # 'emit' types don't have vortex or turbulence            

            # add a force effector at the anchor location and move it into
            # this field's effector collection so it doesn't affect other fields
            loc = (self.anchor.location.x, self.anchor.location.y, self.anchor.location.z)
            bpy.ops.object.effector_add(type='FORCE', location=loc)
            self.em_object = bpy.context.active_object        

            # name and move into the asset collection  
            #move_to_collection(self.em_object, coll_field_name)                           
            self.em_object.name = f"{self.name}Force"
        
            self.coll_name = SYSTEMS[(self.mode, self.z_sign)]["asset"]
            
            coll = self.get_or_create_collection(self.coll_name) 
            
            # unlink from any other collections and link to the asset collection
            for a in list(self.em_object.users_collection):
                #print('self.em_object.users_collection :',self.em_object.users_collection)
                #Outputs:
                #self.em_object.users_collection : (bpy.data.scenes['Scene'].collection,)
                #self.em_object.users_collection : (bpy.data.scenes['Scene'].collection,)
                
                try:
                    a.objects.unlink(self.em_object)
                except Exception:
                    pass
            coll.objects.link(self.em_object)        

            # parent to the field anchor
            try:
                self.em_object.parent = self.anchor
            except Exception:
                pass
       
            #print(self.__dict__)
            #{'anchor': bpy.data.objects['TopEmAnchor'], 
            #'emitter': bpy.data.objects['TopEmEmitter'], 
            #'charge_mesh': bpy.data.meshes['TopEmChargeMesh'], 
            #'charge_obj': bpy.data.objects['TopEmChargeObject'], 
            #'settings': bpy.data.particles['TopEMChargeSettings'], 
            #'em_object': bpy.data.objects['TopEmForce'], 
            #'vortex_object': None, 
            #'turbulence_object': None, 
            #'coll_name': 'TopEmAssets', 'name': 'TopEm', 'z_sign': 1, 'mode': 'emit', 'hemi_radius': 4.0, 'spin': 1}
            #{'anchor': bpy.data.objects['BottomEmAnchor'], 'emitter': bpy.data.objects['BottomEmEmitter'], 'charge_mesh': bpy.data.meshes['BottomEmChargeMesh'], 'charge_obj': bpy.data.objects['BottomEmChargeObject'], 'settings': bpy.data.particles['BottomEMChargeSettings'], 'em_object': bpy.data.objects['BottomEmForce'], 'vortex_object': None, 'turbulence_object': None, 'coll_name': 'BottomEmAssets', 'name': 'BottomEm', 'z_sign': -1, 'mode': 'emit', 'hemi_radius': 4.0, 'spin': -1}

            return self.em_object

            
        if self.mode == "vortex":

            self.settings.normal_factor = 1.0 * self.z_sign             
            # Allows the vortex particles to properly emerge 'inward' (positive value)       
            #self.settings.effector_weights.gravity = 0.75 * self.z_sign
            self.settings.effector_weights.gravity = 0.9 * self.z_sign
            # Lets vortex particles pass 5 beyond the proton before dissapearing
            
            # Single anchor location for both 'VORTEX' and 'TURBULENCE' effector forces
            loc = (self.anchor.location.x, self.anchor.location.y, self.anchor.location.z)

            bpy.ops.object.effector_add(type='TURBULENCE', location=loc)
            self.turbulence_object = bpy.context.active_object
            self.turbulence_object.name = f"{self.name}Turbulence"
 
            bpy.ops.object.effector_add(type='VORTEX', location=loc)
            self.vortex_object = bpy.context.active_object
            self.vortex_object.name = f"{self.name}Vortex"
            
            #settings.effector_weights.vortex = 1.0
            #self.settings.effector_weights.vortex = 0.5  # Easier to see spiraling V
            self.settings.effector_weights.turbulence = 1.0

            if self.turbulence_object:
                self.turbulence_object.field.strength = 1.0   # No +/- change
                self.turbulence_object.field.size = 0.6
                self.turbulence_object.field.flow = 1.0
                #turb_obj.parent = anchor

            if self.vortex_object:                
                self.vortex_object.field.strength = self.spin * 1.75   # Good left or righthand
                self.vortex_object.field.distance_max = BASE_RADIUS * 1.1     
                self.vortex_object.field.falloff_type = 'SPHERE'
                
            self.coll_name = SYSTEMS[(self.mode, self.z_sign)]["asset"]

            coll = self.get_or_create_collection(self.coll_name) 

            for a in list(self.vortex_object.users_collection):
                try:
                    a.objects.unlink(self.vortex_object)
                except Exception:
                    pass
            coll.objects.link(self.vortex_object)

            # move self.turbulence_object into effectors collection
            for b in list(self.turbulence_object.users_collection):
                try:
                    b.objects.unlink(self.turbulence_object)
                except Exception:
                    pass
            coll.objects.link(self.turbulence_object)

            try:
                self.turbulence_object.parent = self.anchor
                self.vortex_object.parent = self.anchor
            except Exception:
                pass            

            #print(self.__dict__)
            
            return self.vortex_object, self.turbulence_object 
          

    def build(self, cfg):  

        self.create_anchor(cfg) 
        
        self.create_profiled_hemi_emitter(cfg)
        
        self.create_charge_mesh(cfg)

        self.assign_charge_spin_color(cfg)

        self.add_particle_system_to_emitter(cfg) 

        self.add_force_fields(cfg)  

        return 
    
    ###### ParticleField End ######
    
        
def apply_state_to_proton():

    proton = (
        bpy.data.objects.get("RProton_spin")
        or bpy.data.objects.get("LProton_spin")
        # or bpy.data.objects.get("NoProton_spin")
    )

    if proton is None:
        return

    proton["spin_rate"] = STATE.spin_rate
    proton["spin_accel"] = STATE.spin_accel

    proton.rotation_euler.z += STATE.spin_rate

    update_proton_spin_color(proton)
    

# --------------------------------
# load_post handler
# --------------------------------

@persistent
def load_post_handler(dummy):
    
    global FLOW
    
    print("load_post_handler fired")
    
    FLOW = ChargeFlowController()
    
    bpy.app.timers.register(
        delayed_flow_setup,
        first_interval = 1.0
    )


def register_load_handler():
    ''' This function is not called, 21 Jun '''
    print("register_load_handler CALLED")
    
    handlers = bpy.app.handlers.load_post
    
    print("before append:", handlers)     
    
    for h in list(handlers):    
        if getattr(h, "__name__", "") == "load_post_handler":    
            handlers.remove(h)
       
    handlers.append(load_post_handler)
    
    print("AFTER append:", handlers) 


def delayed_flow_setup():
    
    global FLOW
    
    print("delayed_flow_setup")
    
    proton = (
        bpy.data.objects.get("RProton_spin")
        or bpy.data.objects.get("LProton_spin")
        # or bpy.data.objects.get("NoProton_spin")
    )
    
    if proton is None:
        print("proton not ready")
        return 0.25    # delay
    
    register_flow_handler()
    
    print("flow handler registered")
    
    return None


# -----------------------------
# Animation handler
# -----------------------------
# ChatGPT: the charge_flow_handler() contains the entire architecture 
# in one place.
# ChatGPT wrote. that STATE.update() belongs inside this frame handler, 
# immediately after the controller gathers measurements and before any 
# Blender objects are modified.
###ME. Done
@persistent
def charge_flow_handler(scene):
    # With changes reflecting the ProtonState and ParticleField classes
    
    FLOW.update()
    # I repeat, this stuff is magic.    
    
# -----------------------------
# Helper to register the handler
# -----------------------------

def register_flow_handler():
    
    handlers = bpy.app.handlers.frame_change_pre
    
    # remove dupes safely
    for h in list(handlers):
        if getattr(h, "__name__", "") == "charge_flow_handler":
            handlers.remove(h)
            
    handlers.append(charge_flow_handler
    )
    

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
# Proton spin materials
# -----------------------------  
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

def get_mat(name):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = ensure_materials()[name]
    return mat

def update_proton_spin_color(proton_empty):
    #Switch proton material based on current spin direction.
    #Positive spin = red, Zero spin = white, Negative spin = blue
    if not proton_empty:
        return
    # proton mesh is the child of the spin empty
    proton_mesh = None
    for child in proton_empty.children:
        if child.type == 'MESH':
            proton_mesh = child
            break
    if not proton_mesh:
        return
    spin_rate = proton_empty.get("spin_rate", 0.0)
    near_zero = 0.025

    #desired_mat = bpy.data.materials.get("RSpin") or ensure_materials()["RSpin"]
    if spin_rate > near_zero:
        desired_mat = get_mat("RSpin")
    elif near_zero >= spin_rate and spin_rate > - near_zero:
        desired_mat = get_mat("Emission")	
    elif  - near_zero >= spin_rate: 
        desired_mat = get_mat("LSpin")    
    else:
        return     
    
    if proton_mesh.data.materials:
        proton_mesh.data.materials[0] = desired_mat
    else:
        proton_mesh.data.materials.append(desired_mat)

# -----------------------------
# utility functions
# -----------------------------

#def move_to_collection(obj, coll_name): 
#    coll = bpy.data.collections.get(coll_name)
#    if not coll:
#        coll = bpy.data.collections.new(coll_name)
#        bpy.context.scene.collection.children.link(coll)

#    # unlink from all current collections
#    for c in obj.users_collection:
#        c.objects.unlink(obj)
#    coll.objects.link(obj)
#    return


def remove_all_collections():
    #print("--- Removing all collections ---")
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
        #print('o.name = ', o.name, ' removed and unlinked')        
        bpy.data.objects.remove(o, do_unlink=True)
    # also remove particle systems data-blocks if present
    for ps in list(bpy.data.particles):
        # ps.name =  BottomVortexChargeSettings are not yet removed
        #print('ps.name = ', ps.name)        
        if (ps.name.startswith("TopVortex") or (ps.name.startswith("BottomVortex"))):
            #print('ps.name = ', ps.name, ' removed')   
            bpy.data.particles.remove(ps)
    # remove meshes named by script
    for m in list(bpy.data.meshes):
        #print('m.name = ', m.name) 
        if (m.name.startswith("TopVortex") or (m.name.startswith("BottomVortex"))):        
            #print('m.name = ', m.name, ' removed')   
            bpy.data.meshes.remove(m)


def remove_all_objects():
    #print("--- Removing all objects ---")
    for _obj in list(bpy.data.objects):
        bpy.data.objects.remove(_obj, do_unlink=True)


def purge_orphans():
    #print("--- Purging orphaned datablocks (Outliner) ---")
    try:
        bpy.ops.outliner.orphans_purge(
            do_local_ids=True,
            do_linked_ids=False,
            do_recursive=True
        )
    except RuntimeError:
        pass


def remove_charge_groups(): 
    #remove_handler()  # Use only manually
    clear_previous()
    remove_all_objects()
    remove_all_collections()
    purge_orphans()  
    # The hdri flat western plain remains.
    # remove any created particle instance object
    
    ###ME. See some possible candidates for class field obj conversion.
    # 'TopEm': <__main__.ParticleField object at 0x0000027D67482950>, 
    # 'BottomEm': <__main__.ParticleField object at 0x0000027D6705A6D0>, 
    # 'TopVortex': <__main__.ParticleField object at 0x0000027D67053950>, 
    # 'BottomVortex':  <__main__.ParticleField object at 0x0000027D64CD3950>    
     
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

def add_proton_grp(loc_x, loc_y, loc_z, type='L'):  
    spin_dir = type
    collection_name = f"Proton_Collection"
    My_collection = bpy.data.collections.new(collection_name)    
    bpy.context.scene.collection.children.link(My_collection)

    # Step 1: Create orbit empty at origin
    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=0.15, location=(loc_x, loc_y, loc_z))
    porbit_empty = bpy.context.active_object
    porbit_empty.name = f"{type}Proton_spin"    
    porbit_empty["spin_rate"] = 0.0 

    # Step 2: Create proton at offset relative to empty
    bpy.ops.mesh.primitive_uv_sphere_add(radius=P_RADIUS, location=(loc_x, loc_y, loc_z))
    proton = bpy.context.active_object
    proton.name = f"{type}proton"
    proton.data.name = f"{type}proton"
    proton.data.materials.append(get_mat("LSpin" if spin_dir == "L" else "RSpin"))   # Solid proton colors

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
        
        bpy.ops.object.shade_smooth() 
        bpy.context.view_layer.objects.active = proton
        proton.select_set(True)
        bpy.ops.object.join()

    My_collection.objects.link(porbit_empty)
    My_collection.objects.link(proton)
    return porbit_empty, proton


#####################################################
# Manually un-comment individual functions, Then 
# re-comment out that function(s) and move to the next.
######################################################

# 1. Either press "a" and "x", to delete objects, then selecting and 
# deleting collections; then "File" "Clean Up" and "Purge Unused Data"; 
# remove_charge_groups() does all that.
#remove_charge_groups()  #############

# 2. Add a camera. At a location and orientation. Given "overcast_soil_2_4k.exr" 
# and a good view of the horizon and sky toward -X, I then positioned
# the camera directly across the top_vortex at the origin at +X=100. ...
# Uncomment the 3 lines and run
#loc = (200, 0, -45)  # Good spot
#rot = (1.775, 0, 1.55)
#setup_camera(loc, rot)  #############

# 3. 'Procedural function' version's functions have been removed, & related cleanup. 

# 4. The HDRI background image needs to be located in a separate 
# folder, here /Users/ME/hdris also see the # HDRI Functions, section above.
#path_to_image = str(pathlib.Path.home()/"hdris"/"overcast_soil_4k.exr")
#path_to_image = str(pathlib.Path.home()/"hdris"/"overcast_soil_2_4k.exr")
#path_to_image = str(pathlib.Path.home()/"hdris"/"approaching_storm_4k.exr")
#apply_hdri(str(pathlib.Path.home()/"hdris"/"overcast_soil_2_4k.exr"))  
###ME. Somehow, without me un-commenting and running the HDRI functs the blend 
# file finds and adds the 'overcast_soil_2_4k.exr' rendering image on it's own(?)
# Maybe saving each new blend file as 'Save As' is not overwritting saved HDRI info.

# 5. In case lights are needed
#two_lights()

# 6. Add the spinning, charge recycling proton
#loc_x, loc_y, loc_z = 0, 0, 0
#proton_empty, proton_mesh  = add_proton_grp(loc_x, loc_y, loc_z, type='R', spin_mat=spin_mat_r)   ######### Right spin proton
#proton_empty, proton_mesh  = add_proton_grp(loc_x, loc_y, loc_z, type='L', spin_mat=spin_mat_l)   ######### Left spin proton   

# Or Press 'Run Script', the below script does most of that without uncommenting. 

if __name__ == "__main__":

    remove_charge_groups() 
    ensure_materials() 
    
    loc_x, loc_y, loc_z = 0, 0, 0
    #loc_x, loc_y, loc_z = 10, 10, 0
    
    proton_empty, proton_mesh = add_proton_grp(loc_x, loc_y, loc_z, type='R')
    update_proton_spin_color(proton_empty)   # proton w no spin, initially white.
    # Eventually the proton will consist of itself as well as its 4 particle systems.
    
    particle_fields = {}   # Creating a particle_fields 'registry'.
    
    # Choose EMITTERS_LEFT. Bottom, l spinning vortex and particles, Top, r spinning vortex and particles. 
    # Or EMITTERS_RIGHT. Bottom, r spinning vortex and particles, Top, l spinning vortex and particles. 
    
    #for cfg in EMITTERS_LEFT:   
    for cfg in EMITTERS_RIGHT:   
        field = ParticleField(cfg)
        field.build(cfg) 
        particle_fields[field.name] = field       
    
    FLOW = ChargeFlowController(particle_fields)
    
    ## ONLY delayed registration should exist. 
    bpy.app.timers.register(
        delayed_flow_setup,
        first_interval=1.0
    )

    print("MAIN finished")
    
    # The usual System Console output upon 'Running the Script' is:
    #Info: Deleted 9 data-block(s)    ### Subsequent 'Runs' output 'Deleted 17 data-...'
    #MAIN finished  
    #delayed_flow_setup
    #flow handler registered      
    
    # Many print() statements here and throughout the script were added to better 
    # learn/understand the present object oriented class architecture.
    # I've since removed most of the 'known good' transcribed console print outputs 
    # but left the commented-out print()'s in-place if/as/when needed. 
    
    #print('ParticleField.field_names =', ParticleField.field_names)    
    #print('particle_fields = ', particle_fields)     
    # Outputs:
    #ParticleField.field_names = ['TopEm', 'BottomEm', 'TopVortex', 'BottomVortex']
    #particle_fields =  {
    # 'TopEm': <__main__.ParticleField object at 0x0000027D67482950>, 
    # 'BottomEm': <__main__.ParticleField object at 0x0000027D6705A6D0>, 
    # 'TopVortex': <__main__.ParticleField object at 0x0000027D67053950>, 
    # 'BottomVortex':  <__main__.ParticleField object at 0x0000027D64CD3950>
    #}    
        
    ###Chat GPT wrote. "Before changing `ChargeFlowController`, I'd put 
    # some temporary tests" immediately after creating the registry:
    #print("Particle field registry:")
    #for name, field in particle_fields.items():
    #    print(name, "->", field)

    #Then test one level deeper:
    #print("TopVortex emitter:", particle_fields["TopVortex"].emitter)
    #print("BottomVortex anchor:", particle_fields["BottomVortex"].anchor)   
    #print("TopEM settings :", particle_fields["TopEm"].settings)
    #print("BottomEM force:", particle_fields["BottomEm"].em_object)    
     
    ###ME. When uncommmented and 'Run', these 2 originally 'temporary tests' 
    # outputs to the system console; ('Window', 'Toggle System Console').     
    
    
'''   
# After the scene has completed a full 1000 frame run, add some randomness 
# and hide the ps emitters with these console commands:

bpy.data.particles["TopEMChargeSettings"].distribution = 'RAND'
bpy.data.objects["TopVortexEmitter"].show_instancer_for_viewport = False 
bpy.data.objects["BottomVortexEmitter"].show_instancer_for_viewport = False
bpy.data.objects["TopEmEmitter"].show_instancer_for_viewport = False 
bpy.data.objects["BottomEmEmitter"].show_instancer_for_viewport = False 

'''

