import bpy
import bmesh
import math
import random

bl_info = {
    "name": "Coral Generator",
    "author": "Denny Lang, Leon Herrmann",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "View3D > Add > Mesh > Add Coral",
    "description": "An addon to create different types of corals",
    "category": "Add Mesh",
    "support": "TESTING",
}

class Params:
    """Parameters for the Coral"""
    RADIUS = 40
    FRINGES = 50

def brainCoral(radius, fringes): 
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)
    bpy.ops.outliner.orphans_purge()

    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    current_mesh = bpy.context.object.data
    counter = 1

    for vert in current_mesh.vertices:  
        
        if vert.co.z < vert.co.z / 2:
            vert.co.z = - radius / 2
        
        counter += 1
            
    bpy.ops.object.editmode_toggle()

    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    
    vertices = 0
    while vertices < fringes:  
        bpy.ops.mesh.select_all(action='DESELECT')
        selectedVert = random.randint(0, counter)
        bpy.ops.mesh.select_random(ratio=0.004, seed=selectedVert)
        for v in bm.verts:
            if v.co.z > 0 and v.co.z < radius - (radius / 10 ):
                if v.select:
                    print('Transformed')
                    bpy.context.scene.transform_orientation_slots[0].type = 'NORMAL'
                    bpy.ops.transform.translate(value=(0,0,2), orient_axis_ortho='X', orient_type='NORMAL')
                    vertices += 1

    bpy.ops.object.editmode_toggle()

    # Texture 
    brainTexture = bpy.data.materials.new(name= "BrainCoral")
    brainTexture.use_nodes = True
    mout = brainTexture.node_tree.nodes.get('Material Output')
    princ1 = brainTexture.node_tree.nodes.get('Principled BSDF')
    princ2 = brainTexture.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
    colRamp1 = brainTexture.node_tree.nodes.new("ShaderNodeValToRGB")
    colRamp2 = brainTexture.node_tree.nodes.new("ShaderNodeValToRGB")
    mixShader1 = brainTexture.node_tree.nodes.new("ShaderNodeMixShader")
    mixShader2 = brainTexture.node_tree.nodes.new("ShaderNodeMixShader")
    glossy = brainTexture.node_tree.nodes.new("ShaderNodeBsdfGlossy")
    bump = brainTexture.node_tree.nodes.new("ShaderNodeBump")
    texMus = brainTexture.node_tree.nodes.new("ShaderNodeTexMusgrave")
    texCoord = brainTexture.node_tree.nodes.new("ShaderNodeTexCoord")
    mapping = brainTexture.node_tree.nodes.new("ShaderNodeMapping")

    # Texture links
    brainTexture.node_tree.links.new(texCoord.outputs[3], mapping.inputs[0])
    brainTexture.node_tree.links.new(mapping.outputs[0], texMus.inputs[0])
    brainTexture.node_tree.links.new(texMus.outputs[0], colRamp1.inputs[0])
    brainTexture.node_tree.links.new(texMus.outputs[0], colRamp2.inputs[0])
    brainTexture.node_tree.links.new(texMus.outputs[0], mixShader1.inputs[0])
    brainTexture.node_tree.links.new(texMus.outputs[0], bump.inputs[2])
    brainTexture.node_tree.links.new(bump.outputs[0], princ1.inputs[22])
    brainTexture.node_tree.links.new(colRamp1.outputs[0], princ1.inputs[0])
    brainTexture.node_tree.links.new(colRamp1.outputs[0], mixShader2.inputs[0])
    brainTexture.node_tree.links.new(glossy.outputs[0], mixShader1.inputs[2])
    brainTexture.node_tree.links.new(princ1.outputs[0], mixShader1.inputs[1])
    brainTexture.node_tree.links.new(colRamp2.outputs[0], princ2.inputs[3])
    brainTexture.node_tree.links.new(princ2.outputs[0], mixShader2.inputs[2])
    brainTexture.node_tree.links.new(mixShader1.outputs[0], mixShader2.inputs[1])
    brainTexture.node_tree.links.new(mixShader2.outputs[0], mout.inputs[0])

    #Texture Default wertes
    mapping.inputs[3].default_value = (0.1, 0.1, 0.1)
    texMus.inputs[1].default_value = 4.9
    texMus.inputs[4].default_value = 1
    texMus.inputs[6].default_value = 0
    texMus.musgrave_type = 'RIDGED_MULTIFRACTAL'
    bump.inputs[1].default_value = 0.6
    princ1.inputs[9].default_value = 0.18
    princ1.inputs[13].default_value = 0.37
    princ1.inputs[17].default_value = 0.027
    princ1.inputs[18].default_value = 0.668
    princ1.inputs[20].default_value = 0
    glossy.inputs[1].default_value = 0.612
    princ2.inputs[9].default_value = 0.7
    princ2.inputs[17].default_value = 0.53
    princ2.inputs[18].default_value = 0.7

    #Color 
    firstColor = (0.456, 0.44, 0, 1)
    secondColor = (0.015, 0.012, 0, 1)
    thirdColor = (0.5, 0.427, 0.078, 1)
    fourthColor= (1, 1, 0.4, 1)

    colRamp1.color_ramp.elements[0].position = 0
    colRamp1.color_ramp.elements[1].position = 0.034
    colRamp1.color_ramp.elements.new(0.227)
    colRamp1.color_ramp.elements.new(1)
    colRamp1.color_ramp.elements[0].color = firstColor
    colRamp1.color_ramp.elements[1].color = secondColor
    colRamp1.color_ramp.elements[2].color = thirdColor
    colRamp1.color_ramp.elements[3].color = fourthColor

    colorRosa = (1, 0.5, 0.967, 1)
    colorYellow = (1, 0.984, 0.474, 1)
    colorGreen = (0, 0.5, 0, 1)

    princ2.inputs[0].default_value = colorYellow


    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 3
    current_mesh.update()




class simpleBrainCoral():
    #TODO MAIN
    bl_idname = "object.simple_brain_coral"
    bl_label = "Simple Brain Coral"

    radius: bpy.props.IntProperty(
        name="Radius",
        description="radius of the coral",
        default = 20)
    
    fringes: bpy.props.IntProperty(
        name="Fringes",
        description="fringes of the coral",
        default = 20)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, radius, fringes):
        brainCoral(radius, fringes)
        return {'FINISHED'}

    

    
def addMenu(self, context):
    self.layout.operator(simpleBrainCoral.bl_idname,
                         text="Add Brain Coral")
    
#register, unregister = bpy.utils.register_classes_factory(classes)
def register():
    bpy.utils.register_class(Params)
    bpy.utils.register_class(simpleBrainCoral)
    bpy.types.VIEW3D_MT_mesh_add.append(addMenu)


def unregister():
    bpy.utils.unregister_class(Params)
    bpy.utils.unregister_class(simpleBrainCoral)
    bpy.types.VIEW3D_MT_mesh_add.remove(addMenu)
