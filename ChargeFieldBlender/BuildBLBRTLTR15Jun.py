import bpy
import random
import numpy as np
import math

e_radius = 0.2 
e_locz = 1.2  # above or below a proton pole

spin_mat_r = bpy.data.materials.new('RSpin')
spin_mat_r.diffuse_color = (1.0, 0.0, 0.0, 1.0)
spin_mat_l = bpy.data.materials.new('LSpin')
spin_mat_l.diffuse_color = (0.0, 0.0, 1.0, 1.0)
emission_mat = bpy.data.materials.new('Emission')
emission_mat.diffuse_color = (1.0, 1.0, 1.0, 0.5)
text_mat = bpy.data.materials.new('Text')
text_mat.diffuse_color = (1.0, 1.0, 1.0, 0.0)

# =============================
# Component creator functions
# =============================

def add_proton(loc_x, loc_y, loc_z):
    '''The proton'''
    bpy.ops.mesh.primitive_uv_sphere_add(location=(loc_x, loc_y, loc_z)) 
    bpy.ops.object.shade_smooth()    
    return bpy.context.active_object

def add_electron(loc_x, loc_y, loc_z):
    '''The proton's captured electron'''
    bpy.ops.mesh.primitive_uv_sphere_add(radius=e_radius, location=(loc_x, loc_y, loc_z))   
    bpy.ops.object.shade_smooth()
    return bpy.context.active_object

def add_emission(loc_x, loc_y, loc_z): 
    '''The proton's equatorial emissions'''                        
    bpy.ops.mesh.primitive_cylinder_add(radius=3, depth=0.05, location=(loc_x, loc_y, loc_z))
    return bpy.context.active_object

def add_intake(loc_x, loc_y, loc_z, x_coef=1, z_coef=1):
    '''The proton's main spiral charge intake into the electron vacant proton pole'''
    # type:+/- coef_x, +/- coef_z. BL:+x,+z; TL:+x,-z; BR:-x,+z; TR:-x,-z.
    # Set time 't' axis
    t = np.arange(1.05, 5, 0.01)
    # Set curve coordinates
    points = np.zeros((len(t), 3))
    for N in range(len(t)):
        x = x_coef*0.32*(1 - t[N]) * np.cos(5 * t[N])
        y = 0.32*(1 - t[N]) * np.sin(5 * t[N])
        z = z_coef*0.6*t[N]
        points[N] = [x, y, z]
    # Create the curve and set its points
    curve_data = bpy.data.curves.new(name='ParametricLine', type='CURVE')
    polyline = curve_data.splines.new('POLY')
    polyline.points.add(len(points) - 1)
    for N in range(len(points)):
        x, y, z = points[N]
        polyline.points[N].co = (x, y, z, 1)
    curve_object = bpy.data.objects.new('ParametricLine', curve_data)
    bpy.context.collection.objects.link(curve_object)
    # Make the spiral the active object.
    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get('ParametricLine')
    if obj:
        obj.select_set(True)  # Select the object
        bpy.context.view_layer.objects.active = obj  # Set it as the active object
    # Give the curve thickness
    obj.data.bevel_depth = 0.05
    # Convert the curve into a mesh.
    bpy.ops.object.convert(target='MESH') 
    obj.location=(loc_x, loc_y, loc_z)
    return bpy.context.active_object

# =============================
# Proton group creator functions
# =============================

def add_proton_electron_emission_intake(loc_x, loc_y, loc_z, eloc_z=-e_locz, type = 'BL', spin_mat = spin_mat_l, x_coef=1, z_coef=1):
    collection_name = f"{type}_Collection"
    My_collection =  f"My_{type}_collection" 
    My_collection = bpy.data.collections.new(collection_name)    
    bpy.context.scene.collection.children.link(My_collection)
    # add proton
    proton = f"{type}proton"
    proton = add_proton(loc_x, loc_y, loc_z) 
    proton = bpy.context.active_object
    proton.data.name = f"{type}proton"    
    proton.name = f"{type}proton"     
    proton.data.materials.append(spin_mat)  
    My_collection.objects.link(proton)
    # add electron
    electron = f"{type}electron" 
    electron = add_electron(loc_x, loc_y, loc_z + eloc_z)      
    electron = bpy.context.active_object
    electron.data.name = f"{type}electron"
    electron.name = f"{type}electron"  
    electron.data.materials.append(spin_mat)       
    My_collection.objects.link(electron)    
    # add emission
    emission = f"{type}emission"     
    emission = add_emission(loc_x, loc_y, loc_z)
    emission = bpy.context.active_object
    emission.data.name = f"{type}emission"
    emission.name = f"{type}emission"   
    emission.data.materials.append(emission_mat)     
    My_collection.objects.link(emission)    
    # add intake
    intake = f"{type}intake"  
    intake = add_intake(loc_x, loc_y, loc_z, x_coef, z_coef)
    # type:+/-,coef_x,+/-coef_z. BL:+x,+z; TL:+x,-z; BR:-x,+z; TR:-x,-z. 
    intake = bpy.context.active_object
    intake.data.name = f"{type}intake"
    intake.name = f"{type}intake"
    intake.data.materials.append(spin_mat) 
    My_collection.objects.link(intake) 
    bpy.ops.object.select_all(action='DESELECT')  
    #bpy.ops.object.select_all(action='SELECT')    
    return 

# Turn this into a class
# type:+/-,coef_x,+/-coef_z. BL:+x,+z; TL:+x,-z; BR:-x,+z; TR:-x,-z.
def build_TL(loc_x=0.0, loc_y=0.0, loc_z=0.0): # The proton group, not an instance 
    add_proton_electron_emission_intake(
        loc_x, loc_y, loc_z, 
        eloc_z=e_locz, 
        type = 'TL', 
        spin_mat = spin_mat_l, 
        x_coef=1, z_coef=-1)
    return bpy.context.active_object

def build_BL(loc_x=0.0, loc_y=0.0, loc_z=0.0): # The proton group, not an instance 
    add_proton_electron_emission_intake(
        loc_x, loc_y, loc_z, 
        eloc_z=-e_locz, 
        type = 'BL', 
        spin_mat = spin_mat_l, 
        x_coef=1, z_coef=1)
    return bpy.context.active_object

def build_TR(loc_x=0.0, loc_y=0.0, loc_z=0.0): # The proton group, not an instance 
    add_proton_electron_emission_intake(
        loc_x, loc_y, loc_z, 
        eloc_z=e_locz, 
        type = 'TR', 
        spin_mat = spin_mat_r, 
        x_coef=-1, z_coef=-1)
    return bpy.context.active_object

def build_BR(loc_x=0.0, loc_y=0.0, loc_z=0.0): # The proton group, not an instance 
    add_proton_electron_emission_intake(
    loc_x, loc_y, loc_z, 
        eloc_z=-e_locz, 
        type = 'BR', 
        spin_mat = spin_mat_r, 
        x_coef=-1, z_coef=1)
    return bpy.context.active_object

# =============================
# Proton Instance creator functions
# =============================

def instance_collection(collection, location, instance_name):
    empty = bpy.data.objects.new(name=instance_name, object_data=None)
    empty.instance_type = 'COLLECTION'
    empty.instance_collection = collection
    empty.location = location
    bpy.context.scene.collection.objects.link(empty)
    bpy.ops.object.select_all(action='SELECT')  
    return

def build_all_stacks(stacks, spacing=10, loc_x=0.0, loc_y=0.0, loc_z=0.0):
    group_collections = {
        'TR': 'TR_Collection',
        'TL': 'TL_Collection',
        'BR': 'BR_Collection',
        'BL': 'BL_Collection'
    }
    spacing = spacing
    for stack_number, (stack_text, _) in enumerate(stacks):
        row = stack_number // 12
        col = stack_number % 12
        base_x = loc_x + 10 + col * spacing 
        base_y = loc_y + row * spacing
        group_list = [stack_text[i:i+2] for i in range(0, len(stack_text), 2)]
        #print(f"Building stack {stack_number + 1} at position ({base_x}, {base_y}) with groups: {group_list}")
        for level, group in enumerate(group_list):
            collection_name = group_collections.get(group)
            if collection_name is None:
                print(f"Unknown group: {group}")
                continue
            z = loc_z -level * spacing
            instance_name = f"{group}_Stack{stack_number}_Level{level}"
            #print(instance_name)
            instance_collection(bpy.data.collections[collection_name], (base_x, base_y, z), instance_name)
    return

def place_text_labels(stack_list, grid_size=12, cell_size=10.0, z_height=5.0, loc_x=0.0, loc_y=0.0, loc_z=0.0):
    # Cleanup previous labels
    #for obj in bpy.data.objects:
    #    if obj.name.startswith("Label_"):
    #        bpy.data.objects.remove(obj, do_unlink=True)
    for i, (label_text, _) in enumerate(stack_list):
        # Grid layout (left to right, bottom to top)
        row = i // grid_size
        col = i % grid_size
        x = loc_x + 10 + col * cell_size   
        y = loc_y + row * cell_size
        z = loc_z + z_height
        # Add and configure text object
        bpy.ops.object.text_add(location=(x, y, z))
        text_obj = bpy.context.object
        text_obj.name = f"Label_{i+1}"
        text_obj.data.body = label_text
        # Center text horizontally
        text_obj.data.align_x = 'CENTER'
        text_obj.data.extrude = 0.05
        # View from the -Y direction
        text_obj.rotation_euler[0] = math.radians(90)
        # Convert text to mesh
        bpy.ops.object.convert(target='MESH')
        stack_label = bpy.context.active_object
        stack_label.data.materials.append(text_mat)
        stack_label.select_all(action='SELECT')        
    return bpy.context.active_object                  

def fig1_message(loc_x=0.0, loc_y=0.0, loc_z=0.0, msg='TESTING TESTING 1 2 3'):
    #'Various types of 2 vertically aligned electron-proton configurations',
    #'TLBL      TRTR      TRTL     BRBR       BRBL      TRBL     BRTR     BRTL',
    #'good      good       bad        good        bad         good       bad      bad'    
    list = ['good', 'good', 'bad', 'good', 'bad', 'good', 'bad', 'bad']  
    grid_size=12 
    cell_size=5.0
    z_height=-8.75    
    #for i, (label_text, _) in enumerate(stack_list):
    for i in range(8):
        # Grid layout (left to right, bottom to top)
        row = i // grid_size
        col = i % grid_size
        x = loc_x + 10 + col * cell_size   
        y = loc_y + row * cell_size
        z = loc_z + z_height
        # Add and configure text object
        bpy.ops.object.text_add(location=(x, y, z))
        text_obj = bpy.context.object
        text_obj.name = f"Label_{i+1}"
        text_obj.data.body = list[i]
        # Center text horizontally
        text_obj.data.align_x = 'CENTER'
        #text_obj.data.align_x = 'LEFT'
        text_obj.data.extrude = 0.05
        # Face +Y direction
        text_obj.rotation_euler[0] = math.radians(90)
        # Convert text to mesh
        bpy.ops.object.convert(target='MESH')
        message = bpy.context.active_object
        message.data.materials.append(text_mat)
    return  
        
def Linear_and_Angular_Motion():
    #buildFourProtonGrps()
    add_proton_electron_emission_intake(loc_x=0, loc_y=0, loc_z=0, 
            eloc_z=e_locz, type = 'TR', spin_mat = spin_mat_r, x_coef=-1, z_coef=-1)                   
    # directly adds a TR proton group. 
    #four_stacks = [('TL',1), ('BR',2), ('TR',3), ('BL',4)]
    one_stack = [('TR',3)]
    #place_text_labels(one_stack, loc_x=10.0, loc_y=0.0, loc_z=5.0)
    #Error 
    build_all_stacks(one_stack, spacing=10, loc_x=10.0, loc_y=0.0, loc_z=0.0)
    #place_text_labels(one_stack, loc_x=10.0, loc_y=0.0, loc_z=5.0)
    #Error
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
       if obj.name.startswith("TR_S"):
            obj.select_set(True)
    bpy.context.view_layer.objects.active  = obj
    #bpy.ops.action.interpolation_type(type='LINEAR')
    obj = bpy.context.active_object 
    TR = obj
    #Start
    TR.location.z = 5
    TR.rotation_euler[2] = 0
    # insert keyframe at start_frame
    start_frame = 0
    TR.keyframe_insert("location", frame=start_frame)
    TR.keyframe_insert("rotation_euler", frame=start_frame)
    #Change the cube
    TR.rotation_euler[2] = 2*6.28319
    TR.location.z = 15
    # insert a middle keyframe 
    middle_frame = 90
    TR.keyframe_insert("location", frame=middle_frame)
    TR.keyframe_insert("rotation_euler", frame=middle_frame)    
    #Change the cube
    TR.rotation_euler[2] = 4*6.28319
    TR.location.z = 5
    #End. Insert an end_keyframe
    end_frame = 180
    TR.keyframe_insert("location", frame=end_frame)
    TR.keyframe_insert("rotation_euler", frame=end_frame)
    return
            
def buildFourProtonGrps(loc_x=0, loc_y=0, loc_z=0):
    #bpy.context.scene.cursor.location[0] = -100
    x = bpy.context.scene.cursor.location[0] + loc_x
    y = bpy.context.scene.cursor.location[1] + loc_y 
    z = bpy.context.scene.cursor.location[2] + loc_z
    add_proton_electron_emission_intake(x, loc_y, loc_z, 
            eloc_z=-e_locz, type = 'BL', spin_mat = spin_mat_l, x_coef=1, z_coef=1)    
    add_proton_electron_emission_intake(x, y, z, 
            eloc_z=-e_locz, type = 'BR', spin_mat = spin_mat_r, x_coef=-1, z_coef=1)
    add_proton_electron_emission_intake(x, y, z, 
            eloc_z=e_locz, type = 'TL', spin_mat = spin_mat_l, x_coef=1, z_coef=-1)
    add_proton_electron_emission_intake(x, y, z, 
            eloc_z=e_locz, type = 'TR', spin_mat = spin_mat_r, x_coef=-1, z_coef=-1)                   
    #bpy.context.scene.cursor.location[0] = 0
    
    return bpy.context.active_object    

# =============================
# Special H Configurations
# =============================
    
def present_H_groups(loc_x=0, loc_y=0, loc_z=0):
    '''Display the four: TL,TR,BL,BR configurations in 
    those 4 spatial view positions.'''
    spacing = 5
    lloc_y = 0
    lloc_x = spacing 
    lloc_z = spacing 
    build_BL(loc_x-lloc_x, loc_y+lloc_y, loc_z-lloc_z)                   
    build_TL(loc_x-lloc_x, loc_y+lloc_y, loc_z+lloc_z)        
    build_BR(loc_x+lloc_x, loc_y+lloc_y, loc_z-lloc_z)               
    build_TR(loc_x+lloc_x, loc_y+lloc_y, loc_z+lloc_z)               
    #bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_all(action='SELECT')
    return
    
def good_and_bad_di_Hydrogen_fig1():
    '''Arrange 16 proton groups as per Diatomic Hydrogen fig1.'''
    buildFourProtonGrps()  #Needs the proton groups 
    #('TL',1), ('BR',2), ('TR',3), ('BL',4) # source stacks
    top_row = [('TL',1), ('TR',3), ('TR',3), ('BR',2), ('BR',2), ('TR',3), ('BR',2), ('BR',2)]
    bot_row = [('BL',4), ('TR',3), ('TL',1), ('BR',2), ('BL',4), ('BL',4), ('TR',3), ('TL',1)]
    build_all_stacks(top_row, spacing=5, loc_x=0.0, loc_y=0.0, loc_z=3.75)
    #place_text_labels(top_row, loc_x=10.0, loc_y=0.0, loc_z=5.0)
    build_all_stacks(bot_row, spacing=5, loc_x=0.0, loc_y=0.0, loc_z=-3.75)
    #place_text_labels(bot_row, loc_x=10.0, loc_y=0.0, loc_z=-15.0)
    fig1_message()  # Consider adding two more message lines   
    #'Various types of 2 vertically aligned electron-proton configurations',
    #    'TLBL      TRTR      TRTL     BRBR       BRBL      TRBL     BRTR     BRTL',
    #    'good      good       bad        good        bad         good       bad      bad',    
    # place_text_labels() only uses labels, not commentary
    return

def good_di_Hydrogens():
    '''Arrange 8 proton groups as per Diatomic Hydrogen fig1.'''
    buildFourProtonGrps()  #Needs the proton groups 
    #A_locs = [(-12, 0, z), (-4, 0, z), (4, 0, z), (12, 0, z)]
    #'TL','TR','BR','TR'
    top_row = [('TL',1), ('TR',3), ('BR',2), ('TR',3)]
    build_all_stacks(top_row, spacing=5, loc_x=0.0, loc_y=0.0, loc_z=3.75)
    #place_text_labels(top_row, loc_x=10.0, loc_y=0.0, loc_z=5.0)        
    #'BL','TR','BR','BL'
    bot_row = [('BL',4), ('TR',3), ('BR',2), ('BL',4)]
    build_all_stacks(bot_row, spacing=5, loc_x=0.0, loc_y=0.0, loc_z=-3.75)
    #place_text_labels(bot_row, loc_x=10.0, loc_y=0.0, loc_z=-15.0)
    #Need a good_diH2_message()  #  
    return

def quick_Light():
    bpy.ops.object.light_add(type='AREA', location=(0, -60, 60), rotation=(math.radians(45), 0, 0), scale=(1, 1, 1))
    bpy.context.object.data.size = 30
    bpy.context.object.data.energy = 50000
    bpy.ops.object.light_add(type='AREA', location=(0, -60, -60), rotation=(math.radians(135), 0, 0), scale=(1, 1, 1))
    bpy.context.object.data.size = 20
    bpy.context.object.data.energy = 50000    
    return            

def add_positioned_lights(stacks, spacing=10):  # (threeSix_stacks, spacing_x=10, spacing_y=10)
    #def build_all_stacks(stacks, spacing=10):
    for stack_number, (stack_text, _) in enumerate(stacks):
        # Grid layout (left to right, bottom to top)
        #row = i // grid_size
        #col = i % grid_size
        row = stack_number // 12
        col = stack_number % 12
    #light1(x_loc) = ((#cols + 1)/2)*(col_gap) = 12         
    #x = 10 + col * cell_size  
    x0 = ((col + 1)/2) * spacing          
    x1 = ((col + 1)/2) * spacing
    y0 = -60 + (row/2) * spacing 
    y1 = -60 + (row/2) * spacing 
    z0 = 60  #z_height  
    z1 = -60  #z_height

    bpy.ops.object.light_add(type='AREA', location=(x0, y0, z0), rotation=(math.radians(45), 0, 0), scale=(1, 1, 1))
    bpy.context.object.data.size = 30
    bpy.context.object.data.energy = 50000

    bpy.ops.object.light_add(type='AREA', location=(x1, y1, z1), rotation=(math.radians(135), 0, 0), scale=(1, 1, 1))
    bpy.context.object.data.size = 20
    bpy.context.object.data.energy = 50000
    return

def some_cleanup():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])    
    
    bpy.ops.outliner.orphans_purge() 
    return


all_stacks = [('TL',1), ('BR',2), ('TR',3), ('BL',4),
            ('TLTL',5), ('BRBR',6), ('TRTR',7), ('BLBL',8), ('TLBR',9), ('TRBL',10), 
            ('TRBR',11), ('TLBL',12), ('BLTL',13), ('BRTR',14), ('BLTR',15), ('BRTL',16), 
            ('TLTLTL',17), ('BRBRBR',18), ('TRTRTR',19), ('BLBLBL',20), ('TLBRBR',21), 
            ('TRBLBL',22), ('TRBRBR',23), ('TLBLBL',24), ('TLTLBR',25), ('TRTRBL',26), 
            ('TRTRBR',27), ('TLTLBL',28), ('BLTLTL',29), ('BRTRTR',30), ('BLTRTR',31), 
            ('BRTLTL',32), ('BLBLTL',33), ('BRBRTR',34), ('BLBLTR',35), ('BRBRTL',36), 
            ('TLTLTLTL',37), ('BRBRBRBR',38), ('TRTRTRTR',39), ('BLBLBLBL',40), 
            ('TLBRBRBR',41), ('TRBLBLBL',42), ('TRBRBRBR',43), ('TLBLBLBL',44), ('TLTLBRBR',45), ('TRTRBLBL',46), 
            ('TRTRBRBR',47), ('TLTLTLBL',48), ('TLTLTLBR',49), ('TRTRTRBL',50), ('TRTRTRBR',51), ('TLTLTLBL',52), 
            ('BLTLTLTL',53), ('BRTRTRTR',54), ('BLTRTRTR',55), ('BRTLTLTL',56), ('BLBLTLTL',57), ('BRBRTRTR',58),
            ('BLBLTRTR',59), ('BRBRTLTL',60), ('BLBLBLTL',61), ('BRBRBRTR',62), ('BLBLBLTR',63), ('BRBRBRTL',64), 
            ('TLTLTLTLTL',65), ('BRBRBRBRBR',66), ('TRTRTRTRTR',67), ('BLBLBLBLBL',68), ('TLBRBRBRBR',69), ('TRBLBLBLBL',70),
            ('TRBRBRBRBR',71), ('TLBLBLBLBL',72), ('TLTLBRBRBR',73), ('TRTRBLBLBL',74), ('TRTRBRBRBR',75), ('TLTLBLBLBL',76), 
            ('TLTLTLBRBR',77), ('TRTRTRBLBL',78), ('TRTRTRBRBR',79), ('TLTLTLBLBL',80), ('TLTLTLTLBR',81), ('TRTRTRTRBL',82), 
            ('TRTRTRTRBR',83), ('TLTLTLTLBL',84), ('BLTLTLTLTL',85), ('BRTRTRTRTR',86), ('BLTRTRTRTR',87), ('BRTLTLTLTL',88),
            ('BLBLTLTLTL',89), ('BRBRTRTRTR',90), ('BLBLTRTRTR',91), ('BRBRTLTLTL',92), ('BLBLBLTLTL',93), ('BRBRBRTRTR',94), 
            ('BLBLBLTRTR',95), ('BRBRBRTLTL',96), ('BLBLBLBLTL',97), ('BRBRBRBRTR',98), ('BLBLBLBLTR',99), ('BRBRBRBRTL',100), 
            ('TLTLTLTLTLTL',101), ('BRBRBRBRBRBR',102), ('TRTRTRTRTRTR',103), ('BLBLBLBLBLBL',104), ('TLBRBRBRBRBR',105), 
            ('TRBLBLBLBLBL',106), ('TRBRBRBRBRBR',107), ('TLBLBLBLBLBL',108), ('TLTLBRBRBRBR',109), ('TRTRBLBLBLBL',110), 
            ('TRTRBRBRBRBR',111), ('TLTLBLBLBLBL',112), ('TLTLTLBRBRBR',113), ('TRTRTRBLBLBL',114), ('TRTRTRBRBRBR',115), 
            ('TLTLTLBLBLBL',116), ('TLTLTLTLBRBR',117), ('TRTRTRTRBLBL',118), ('TRTRTRTRBRBR',119), ('TLTLTLTLBLBL',120), 
            ('TLTLTLTLTLBR',121), ('TRTRTRTRTRBL',122), ('TRTRTRTRTRBR',123), ('TLTLTLTLTLBL',124), ('BLTLTLTLTLTL',125), 
            ('BRTRTRTRTRTR',126), ('BLTRTRTRTRTR',127), ('BRTLTLTLTLTL',128), ('BLBLTLTLTLTL',129), ('BRBRTRTRTRTR',130), 
            ('BLBLTRTRTRTR',131), ('BRBRTLTLTLTL',132), ('BLBLBLTLTLTL',133), ('BRBRBRTRTRTR',134), ('BLBLBLTRTRTR',135), 
            ('BRBRBRTLTLTL',136), ('BLBLBLBLTLTL',137), ('BRBRBRBRTRTR',138), ('BLBLBLBLTRTR',139), ('BRBRBRBRTLTL',140), 
            ('BLBLBLBLBLTL',141), ('BRBRBRBRBRTR',142), ('BLBLBLBLBLTR',143), ('BRBRBRBRBRTL',144)]

example_stacks = [('TLTL', 5), ('BRBR', 6), ('TRTR', 7), ('BLBL', 8), 
    ('TLBR', 9), ('TRBL', 10)]
        
threeSix_stacks = [('TL',1), ('BR',2), ('TR',3), ('BL',4),
    ('TLTL', 5), ('BRBR', 6), ('TRTR', 7), ('BLBL', 8), ('TLBR', 9), ('TRBL', 10),
    ('TRBR', 11), ('TLBL', 12), ('BLTL', 13), ('BRTR', 14), ('BLTR', 15), ('BRTL', 16),
    ('TLTLTL',17), ('BRBRBR',18), ('TRTRTR',19), ('BLBLBL',20), ('TLBRBR',21), 
    ('TRBLBL',22), ('TRBRBR',23), ('TLBLBL',24), ('TLTLBR',25), ('TRTRBL',26), 
    ('TRTRBR',27), ('TLTLBL',28), ('BLTLTL',29), ('BRTRTR',30), ('BLTRTR',31), 
    ('BRTLTL',32), ('BLBLTL',33), ('BRBRTR',34), ('BLBLTR',35), ('BRBRTL',36)
]

def main():  # comment out some_cleanup() before running

    quick_Light()
    #add_positioned_lights(stack_set, spacing=10)  
      
    #Linear_and_Angular_Motion() # Ok          
    #buildFourProtonGrps() # Before build_all or place_text
    # Doesn't work in the opossite order, the instance departs 
    # to the -x "cursor location leaving the empty behind. 
    # as is, the animation in't properly lit up, at proton
    # group mass quickly flickers between red and blue. 

    #buildFourProtonGrps()

    #build_all_stacks(threeSix_stacks, spacing=10)
    #Linear_and_Angular_Motion() # Nope 
          
    good_and_bad_di_Hydrogen_fig1() #With (good, good, bad, ...) commentary   
    
    #good_di_Hydrogens()   # Needs message

    #present_H_groups()  # In their suggested spatial locations. The 4 groups are active.
    
    #PLANNED# present_H_instances() # Need to relocate the 4 groups elsewhere 

    #buildFourProtonGrps() # Before buind_all or place_text
      
    #  build_all_stacks() or place_text_labels()                 
    #build_all_stacks(stack_set, spacing=10)   
    #place_text_labels(stack_set)    
    #add_positioned_lights(stack_set, spacing=10) 
    return

#some_cleanup() # Used only by itelf, Errors when run with main().
#ReferenceError: StructRNA of type Material has been removed

#clean_scene()   # same ReferenceError  when run with main().
#ReferenceError: StructRNA of type Material has been removed
# Comment out main first. 

main()  # comment out some_cleanup() before running

#if __name__ == "__main__":  # Won't let some_cleanup() work ???
#    main()




# How do I move the bases elsewhere and still add group instances together with their instance empties? 
### **Solution: Apply Transforms to the Group Objects Before Instancing**
# 1. Create the base group objects at (0,0,0)** — as you’re already doing.
# 2. Parent them to an empty** if needed (e.g., for the TL, TR, BL, BR groups).
# 3. Apply all transforms** so that their world transforms = local transforms (i.e., they're "baked" in place).
# 4. Move the base group empty** (with children) to your desired location *after* transforms are applied.
# This way, the internal offsets are zeroed out at the origin when the collection is instanced.

### Example Python Fix
# Let’s assume you’re creating a group called `Base_TL` and want to move it to a workspace area 
# after creation but keep the instance behavior clean:
# python
import bpy

# 1. Create the group content at (0, 0, 0)
bpy.ops.object.select_all(action='DESELECT')

# Let's say we have a new cube for simplicity
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "BaseCube_TL"

# 2. Create an empty and parent the cube to it
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
empty = bpy.context.active_object
empty.name = "Base_TL"
cube.parent = empty

# 3. Apply transforms to the cube
bpy.context.view_layer.objects.active = cube
cube.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
cube.select_set(False)

# 4. Optionally move the empty and its child to workspace location
empty.location = (-10, 10, 0)  # Move the base group away from origin for cleanliness

# Now if you create a collection from `Base_TL`, and instance it later, it will behave as expected.

### When Creating the Instance

# Make sure the base is in its own collection first
base_collection = bpy.data.collections.new("TL_Group")
bpy.context.scene.collection.children.link(base_collection)
base_collection.objects.link(empty)
base_collection.objects.link(cube)

# Now add an instance somewhere else
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.collection_instance_add(collection="TL_Group", location=(5, 5, 0))

### Summary
# Always build your group *at the origin* (0,0,0).
# Apply transforms before grouping/moving.
# You can move the **empty base group** later without affecting instance alignment.
# The instance inherits the relative positions of objects within the collection,
# so those must be origin-relative when you create the base.
