import bpy
import bmesh
from bpy.types import (Panel, Operator)
import math
from math import radians
import random

bl_info = {
    "name": "Coral Generator",
    "author": "Denny Lang, Leon Herrmann",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "View3D > N",
    "description": "An addon to create different types of corals",
    "category": "Add Mesh",
    "support": "TESTING",
}

def brainCoral(context, radius, fringes): 
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
    if radius < 10:
        texMus.inputs[1].default_value = 14 # größe des Musters
    elif radius > 50:
        texMus.inputs[1].default_value = 2 # größe des Musters
    else:
        texMus.inputs[1].default_value = 5
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

    bpy.context.active_object.data.materials.append(brainTexture)

    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 3
    current_mesh.update()

def tableCoral(context):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)
    bpy.ops.outliner.orphans_purge()

    coral1 = bpy.ops.mesh.primitive_cone_add()
    bpy.data.objects["Cone"].name = "Coral_Obj"
    bpy.data.meshes["Cone"].name = "Coral_mesh"
    coral1 = bpy.context.active_object
    #coral1.rotation_euler[0] += radians(180)

    coral_nodes = coral1.modifiers.new("CoralNodes","NODES")
    #coral_nodes.node_group = bpy.data.node_groups['Coral1_GeoNodes']


    bpy.ops.node.new_geometry_node_group_assign()
    bpy.data.node_groups["Geometry Nodes"].name = "Coral1_GeoNodes"

    coral_nodes.node_group = bpy.data.node_groups['Coral1_GeoNodes']

    bpy.data.node_groups['Coral1_GeoNodes'].nodes.clear()

    coral_base = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeMeshCone")
    coral_base.inputs[0].default_value = 32
    coral_base.inputs[1].default_value = 3
    coral_base.inputs[2].default_value = 1
    coral_base.inputs[3].default_value = 0.7
    coral_base.inputs[4].default_value = 2.9
    coral_base.inputs[5].default_value = 3.3
    coral_base2 = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeMeshCone")
    coral_base2.inputs[0].default_value = 32
    coral_base2.inputs[1].default_value = 3
    coral_base2.inputs[2].default_value = 1
    coral_base2.inputs[3].default_value = 0.3
    coral_base2.inputs[4].default_value = 2
    coral_base2.inputs[5].default_value = 2
    coral1_baseshape = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeMeshCone")
    coral1_baseshape.inputs[0].default_value = 32
    coral1_baseshape.inputs[1].default_value = 3
    coral1_baseshape.inputs[2].default_value = 1
    coral1_baseshape.inputs[3].default_value = 0
    coral1_baseshape.inputs[4].default_value = 3.4
    coral1_baseshape.inputs[5].default_value = 3.3
    coral1_topshape = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeMeshCone")
    coral1_topshape.inputs[0].default_value = 32
    coral1_topshape.inputs[1].default_value = 3
    coral1_topshape.inputs[2].default_value = 1
    coral1_topshape.inputs[3].default_value = 0
    coral1_topshape.inputs[4].default_value = 1.5
    coral1_topshape.inputs[5].default_value = 2
    coral1_slim1 = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeMeshCone")
    coral1_slim1.inputs[0].default_value = 32
    coral1_slim1.inputs[1].default_value = 3
    coral1_slim1.inputs[2].default_value = 1
    coral1_slim1.inputs[3].default_value = 2.5
    coral1_slim1.inputs[4].default_value = 2.5
    coral1_slim1.inputs[5].default_value = 5.5
    coral1_slim2 = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeMeshCone")
    coral1_slim2.inputs[0].default_value = 32
    coral1_slim2.inputs[1].default_value = 3
    coral1_slim2.inputs[2].default_value = 1
    coral1_slim2.inputs[3].default_value = 0.3
    coral1_slim2.inputs[4].default_value = 0.7
    coral1_slim2.inputs[5].default_value = 4.6
    coral2_baseshape = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeMeshCone")
    coral2_baseshape.inputs[0].default_value = 32
    coral2_baseshape.inputs[1].default_value = 3
    coral2_baseshape.inputs[2].default_value = 1
    coral2_baseshape.inputs[3].default_value = 0.5
    coral2_baseshape.inputs[4].default_value = 2.3
    coral2_baseshape.inputs[5].default_value = 1.3
    coral2_topshape = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeMeshCone")
    coral2_topshape.inputs[0].default_value = 32
    coral2_topshape.inputs[1].default_value = 3
    coral2_topshape.inputs[2].default_value = 1
    coral2_topshape.inputs[3].default_value = 0.1
    coral2_topshape.inputs[4].default_value = 1.5
    coral2_topshape.inputs[5].default_value = 2
    coral2_slim1 = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeMeshCone")
    coral2_slim1.inputs[0].default_value = 32
    coral2_slim1.inputs[1].default_value = 3
    coral2_slim1.inputs[2].default_value = 1
    coral2_slim1.inputs[3].default_value = 2.5
    coral2_slim1.inputs[4].default_value = 2.5
    coral2_slim1.inputs[5].default_value = 2.2
    coral2_slim2 = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeMeshCone")
    coral2_slim2.inputs[0].default_value = 32
    coral2_slim2.inputs[1].default_value = 3
    coral2_slim2.inputs[2].default_value = 1
    coral2_slim2.inputs[3].default_value = 0.3
    coral2_slim2.inputs[4].default_value = 0.7
    coral2_slim2.inputs[5].default_value = 4.6

    transform_coral1 = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeTransform")
    transform_coral1.inputs[1].default_value[0] = 0.6 
    transform_coral1.inputs[1].default_value[1] = -1.1 
    transform_coral1.inputs[1].default_value[2] = 0.1 
    c1bTransform = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeTransform")
    c1bTransform.inputs[1].default_value[0] = 0.2 
    c1bTransform.inputs[1].default_value[1] = 1.1 
    c1bTransform.inputs[1].default_value[2] = 3.2
    c1bTransform.inputs[2].default_value[0] = radians(180)
    c1bTransform.inputs[3].default_value[2] = 0.2   
    c1tTransform = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeTransform")
    c1tTransform.inputs[1].default_value[0] = -2.2 
    c1tTransform.inputs[1].default_value[1] = 0.5 
    c1tTransform.inputs[1].default_value[2] = 3.2
    c1tTransform.inputs[2].default_value[0] = radians(180)
    c1tTransform.inputs[3].default_value[0] = 2  
    c1tTransform.inputs[3].default_value[1] = 2  
    c1tTransform.inputs[3].default_value[2] = 0.8   
    c1s1Transform = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeTransform")
    c1s1Transform.inputs[1].default_value[0] = 0 
    c1s1Transform.inputs[1].default_value[1] = 1.1 
    c1s1Transform.inputs[1].default_value[2] = 2
    c1s1Transform.inputs[2].default_value[0] = radians(180)
    c1s2Transform = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeTransform")
    c1s2Transform.inputs[1].default_value[0] = -0.3 
    c1s2Transform.inputs[1].default_value[1] = 1.1 
    c1s2Transform.inputs[1].default_value[2] = 2
    c1s2Transform.inputs[2].default_value[0] = radians(180)
    c1s2Transform.inputs[3].default_value[2] = 0.5
    transform_coral1_base = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeTransform")
    transform_coral1_base.inputs[1].default_value[0] = 0.2
    transform_coral1_base.inputs[1].default_value[1] = 1.1 
    transform_coral1_base.inputs[1].default_value[2] = 3.1
    transform_coral1_base.inputs[2].default_value[0] = radians(180)

    transform_coral2 = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeTransform")
    transform_coral2.inputs[1].default_value[2] = 0.6 
    transform_coral2.inputs[2].default_value[0] = radians(-4.4) 
    transform_coral2.inputs[2].default_value[1] = radians(-4.2)
    transform_coral2.inputs[2].default_value[2] = radians(-261) 
    transform_coral2.inputs[3].default_value[2] = 0.3 
    c2bTransform = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeTransform")
    c2bTransform.inputs[1].default_value[2] = 1.9
    c2bTransform.inputs[2].default_value[0] = radians(180)
    c2bTransform.inputs[3].default_value[2] = 0.3 
    c2tTransform = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeTransform")
    c2tTransform.inputs[1].default_value[2] = 1.9
    c2tTransform.inputs[2].default_value[0] = radians(180)
    c2tTransform.inputs[1].default_value[0] = 1.5 
    c2s1Transform = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeTransform")
    c2s1Transform.inputs[1].default_value[2] = 1.3
    c2s1Transform.inputs[2].default_value[0] = radians(180)
    c2s2Transform = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeTransform")
    c2s2Transform.inputs[1].default_value[2] = 2
    c2s2Transform.inputs[2].default_value[0] = radians(180)
    c2s2Transform.inputs[3].default_value[2] = 0.5
    transform_coral2_base = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeTransform")
    transform_coral2_base.inputs[1].default_value[2] = 1.8
    transform_coral2_base.inputs[2].default_value[0] = radians(180)

    cbasecut = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeMeshBoolean")
    #cbasecut.operation()
    cbaseslim = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeMeshBoolean")
    cbase2cut = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeMeshBoolean")
    cbaseslim2 = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeMeshBoolean")

    combine = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeJoinGeometry")
    material = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new(type="GeometryNodeSetMaterial")
    coral1 = bpy.data.node_groups['Coral1_GeoNodes'].nodes.new('NodeGroupOutput')
    cTexture = bpy.data.materials.new(name= "Korallse")
    cTexture.use_nodes = True
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(transform_coral2.outputs[0], combine.inputs[0])

    Mout = cTexture.node_tree.nodes.get('Material Output')
    prinNode = cTexture.node_tree.nodes.get('Principled BSDF')
    cRamp = cTexture.node_tree.nodes.new('ShaderNodeValToRGB')
    nTexture = cTexture.node_tree.nodes.new('ShaderNodeTexNoise')

    cTexture.node_tree.links.new(cRamp.outputs[0], prinNode.inputs[0])
    cTexture.node_tree.links.new(nTexture.outputs[0], cRamp.inputs[0])
    cTexture.node_tree.links.new(nTexture.outputs[1], Mout.inputs[2])

    prinNode.inputs[1].default_value = 0.25
    nTexture.inputs[2].default_value = 30
    nTexture.inputs[3].default_value = 5
    nTexture.inputs[4].default_value = 0.5
    nTexture.inputs[5].default_value = 3

    #cRamp.color_ramp.elements[0].position = 0.491
    sub_color = (
        0,
        0,
        0,
        1 # Alpha-Wert der Farbe (Intransparenz) - soll hier immer 1 sein
    )
    object_color = (
        0,#0.462,
        0.250,#1,
        0.193,#0.250,
        1 # Alpha-Wert der Farbe (Intransparenz) - soll hier immer 1 sein
    )
    object_color2 = (
        0,#0.355,
        1,#1,
        0.132,#1,
        1 # Alpha-Wert der Farbe (Intransparenz) - soll hier immer 1 sein
    )
    cRamp.color_ramp.elements[0].color = object_color
    cRamp.color_ramp.elements[1].color = object_color2
    cRamp.color_ramp.elements[0].position = 0.541
    cRamp.color_ramp.elements[1].position = 0.461

    material.inputs[2].default_value = cTexture

    bpy.data.node_groups['Coral1_GeoNodes'].links.new(coral_base.outputs[0], transform_coral1_base.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(transform_coral1_base.outputs[0], cbasecut.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(cbasecut.outputs[0], transform_coral1.inputs[0])

    bpy.data.node_groups['Coral1_GeoNodes'].links.new(coral1_baseshape.outputs[0], c1bTransform.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(c1bTransform.outputs[0], cbasecut.inputs[1])

    bpy.data.node_groups['Coral1_GeoNodes'].links.new(coral1_topshape.outputs[0], c1tTransform.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(c1tTransform.outputs[0], cbasecut.inputs[1])

    bpy.data.node_groups['Coral1_GeoNodes'].links.new(coral1_slim1.outputs[0], c1s1Transform.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(coral1_slim2.outputs[0], c1s2Transform.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(c1s1Transform.outputs[0], cbaseslim.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(c1s2Transform.outputs[0], cbaseslim.inputs[1])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(cbaseslim.outputs[0], cbasecut.inputs[1])

    bpy.data.node_groups['Coral1_GeoNodes'].links.new(transform_coral1.outputs[0], combine.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(material.outputs[0], coral1.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(combine.outputs[0], material.inputs[0])


    bpy.data.node_groups['Coral1_GeoNodes'].links.new(coral_base2.outputs[0], transform_coral2_base.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(transform_coral2_base.outputs[0], cbase2cut.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(cbasecut.outputs[0], transform_coral1.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(coral2_baseshape.outputs[0], c2bTransform.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(c2bTransform.outputs[0], cbase2cut.inputs[1])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(coral2_topshape.outputs[0], c2tTransform.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(c2tTransform.outputs[0], cbase2cut.inputs[1])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(coral2_slim1.outputs[0], c2s1Transform.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(coral2_slim2.outputs[0], c2s2Transform.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(c2s1Transform.outputs[0], cbaseslim2.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(c2s2Transform.outputs[0], cbaseslim2.inputs[1])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(cbaseslim2.outputs[0], cbase2cut.inputs[1])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(cbase2cut.outputs[0], transform_coral2.inputs[0])
    bpy.data.node_groups['Coral1_GeoNodes'].links.new(transform_coral2.outputs[0], combine.inputs[0])

def antlerCoral(context):
    #Delete Default Objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)
    bpy.ops.outliner.orphans_purge()

    #Add a mesh and the geometry node group
    lSysCoral = bpy.ops.mesh.primitive_cone_add()
    bpy.data.objects["Cone"].name = "LCoral_Obj"
    bpy.data.meshes["Cone"].name = "LCoral_mesh"
    lSysCoral = bpy.context.active_object
    lSysCoral_nodes = lSysCoral.modifiers.new("LCoralNodes","NODES")
    newSys = bpy.ops.node.new_geometry_node_group_assign()
    bpy.data.node_groups["Geometry Nodes"].name = "LSysCoral_GeoNodes"
    lSysCoral_nodes.node_group = bpy.data.node_groups['LSysCoral_GeoNodes']
    bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.clear()

    #Creating all the nodes and changing default values
    coral_output = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('NodeGroupOutput')
    Input1 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('NodeGroupInput')
    Input2 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('NodeGroupInput')
    Input3 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('NodeGroupInput')
    Baseline = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCurvePrimitiveLine')
    Basecurve = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeResampleCurve')
    SetPos = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeSetPosition')
    pattern = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeTexNoise')
    BasePatternRange = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMapRange')
    minConvert = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMath')
    capAtri = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCaptureAttribute')
    spline = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeSplineParameter')
    combine_xy = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeCombineXYZ')
    BasePatternRange3 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMapRange')
    pattern2 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeTexNoise')
    trimmer = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeTrimCurve')
    capAtri2 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCaptureAttribute')
    spline2 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeSplineParameter')
    MapRange = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMapRange')
    radius = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeSetCurveRadius')
    circle = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCurvePrimitiveCircle')
    c2m = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCurveToMesh')
    curve_graph = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeFloatCurve')
    BasePatternRange4 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMapRange')
    BasePatternRange2 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMapRange')
    multiplay = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMath')
    points = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeInstanceOnPoints')
    cLine = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCurvePrimitiveLine')
    join = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeJoinGeometry')
    tangent = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeInputTangent')
    branch_rotation = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeCombineXYZ')
    rot_to_vektor = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('FunctionNodeAlignEulerToVector')
    rot_branches = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeRotateInstances')
    bc2m = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCurveToMesh')
    bcircle = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCurvePrimitiveCircle')
    Input4 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('NodeGroupInput')
    slim = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMath')
    bradius = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeSetCurveRadius')
    bMapRange = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMapRange')
    bcapAtri = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCaptureAttribute')
    bspline = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeSplineParameter')
    bcurve_graph = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeFloatCurve')
    Texture = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeSetMaterial')

    #Assigned default values
    Baseline.mode = 'DIRECTION'
    Basecurve.inputs[2].default_value = 30
    Baseline.inputs[3].default_value = 3
    minConvert.operation = 'MULTIPLY'
    minConvert.inputs[1].default_value = -1
    multiplay.operation = 'MULTIPLY'
    branch_rotation.inputs[1].default_value = 8
    MapRange.inputs[3].default_value = 1
    MapRange.inputs[4].default_value = 0
    cLine.inputs[1].default_value[2] = 3.5
    points.inputs[5].default_value[1] = radians(69)
    slim.operation = 'MULTIPLY'
    bcircle.inputs[0].default_value = 10
    bcircle.inputs[4].default_value = 0.05
    rot_branches.inputs[2].default_value[0] = radians(36)
    rot_branches.inputs[2].default_value[1] = radians(135)
    rot_branches.inputs[2].default_value[2] = radians(21)
    bMapRange.inputs[3].default_value = 1
    bMapRange.inputs[4].default_value = 0
    pattern.inputs[3].default_value = 12
    pattern2.inputs[3].default_value = 12
    pattern.inputs[4].default_value = 1
    pattern2.inputs[4].default_value = 1

    #Linked all Nodes Together
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Baseline.outputs[0], Basecurve.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Input1.outputs[1], Baseline.inputs[3])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(pattern.outputs[0], BasePatternRange.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(minConvert.outputs[0], BasePatternRange.inputs[3])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Basecurve.outputs[0], capAtri.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(capAtri.outputs[0], SetPos.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(spline.outputs[0], capAtri.inputs[1])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(spline.outputs[0], capAtri.inputs[2])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(BasePatternRange2.outputs[0], minConvert.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(BasePatternRange2.outputs[0], BasePatternRange.inputs[4])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(BasePatternRange.outputs[0], combine_xy.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(pattern2.outputs[0], BasePatternRange3.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(combine_xy.outputs[0], SetPos.inputs[3])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(BasePatternRange3.outputs[0], combine_xy.inputs[1])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(minConvert.outputs[0], BasePatternRange3.inputs[3])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(BasePatternRange2.outputs[0], BasePatternRange3.inputs[4])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(SetPos.outputs[0], trimmer.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(trimmer.outputs[0], coral_output.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(BasePatternRange4.outputs[0], BasePatternRange2.inputs[4])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(SetPos.outputs[0], trimmer.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(trimmer.outputs[0], capAtri2.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(spline2.outputs[0], capAtri2.inputs[2])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(capAtri2.outputs[0], radius.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(MapRange.outputs[0], curve_graph.inputs[1])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(curve_graph.outputs[0], radius.inputs[2])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(radius.outputs[0], c2m.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(circle.outputs[0], c2m.inputs[1])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(capAtri.outputs[1], BasePatternRange2.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(circle.inputs[4], multiplay.outputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(points.inputs[0], capAtri2.outputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(capAtri2.outputs[2], MapRange.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(cLine.outputs[0], points.inputs[2])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(c2m.outputs[0], join.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(curve_graph.outputs[0], points.inputs[6])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(points.outputs[0], rot_branches.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(tangent.outputs[0], rot_to_vektor.inputs[2])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(branch_rotation.outputs[0], rot_to_vektor.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(rot_to_vektor.outputs[0], points.inputs[5])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(rot_branches.outputs[0], bcapAtri.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bradius.outputs[0], bc2m.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bc2m.outputs[0], join.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bcircle.outputs[0], bc2m.inputs[1])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(slim.outputs[0], bcircle.inputs[4])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bcapAtri.outputs[0], bradius.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bspline.outputs[0], bcapAtri.inputs[2])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bcapAtri.outputs[2], bMapRange.inputs[2])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bMapRange.outputs[0], bcurve_graph.inputs[1])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bcurve_graph.outputs[0], bradius.inputs[2])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(join.outputs[0], Texture.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Texture.outputs[0], coral_output.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].inputs[1].name = "Coral Size"
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Input2.outputs[2], BasePatternRange4.inputs[4])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Input2.outputs[3], BasePatternRange4.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(trimmer.inputs[2], Input3.outputs[3])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Input3.outputs[3], MapRange.inputs[3])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Input3.outputs[3], MapRange.inputs[3])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Input3.outputs[3], multiplay.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Input3.outputs[4], multiplay.inputs[1])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Input4.outputs[4], slim.inputs[0])
    bpy.data.node_groups['LSysCoral_GeoNodes'].inputs[2].name = "Max Size"
    bpy.data.node_groups['LSysCoral_GeoNodes'].inputs[3].name = "Growth"
    bpy.data.node_groups['LSysCoral_GeoNodes'].inputs[4].name = "Radius"
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Input4.outputs[5], pattern.inputs[5])
    bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Input4.outputs[5], pattern2.inputs[5])

    #added Texture
    cTexture = bpy.data.materials.new(name= "Korallse")
    cTexture.use_nodes = True
    Mout = cTexture.node_tree.nodes.get('Material Output')
    prinNode = cTexture.node_tree.nodes.get('Principled BSDF')
    cRamp = cTexture.node_tree.nodes.new('ShaderNodeValToRGB')
    nTexture = cTexture.node_tree.nodes.new('ShaderNodeTexNoise')

    cTexture.node_tree.links.new(cRamp.outputs[0], prinNode.inputs[0])
    cTexture.node_tree.links.new(nTexture.outputs[0], cRamp.inputs[0])
    cTexture.node_tree.links.new(nTexture.outputs[1], Mout.inputs[2])

    prinNode.inputs[1].default_value = 0.25
    nTexture.inputs[2].default_value = 30
    nTexture.inputs[3].default_value = 5
    nTexture.inputs[4].default_value = 0.5
    nTexture.inputs[5].default_value = 3

    sub_color = (
        0,
        0,
        0,
        1 
    )
    object_color = (
        0,
        0.250,
        0.193,
        1 
    )
    object_color2 = (
        0,
        1,
        0.132,
        1 
    )
    cRamp.color_ramp.elements[0].color = object_color
    cRamp.color_ramp.elements[1].color = object_color2
    cRamp.color_ramp.elements[0].position = 0.541
    cRamp.color_ramp.elements[1].position = 0.461

    Texture.inputs[2].default_value = cTexture

class simpleBrainCoral(bpy.types.Operator):
    # MAIN
    bl_idname = "object.simple_brain_coral"
    bl_label = "Simple Brain Coral"
    bl_options = {"REGISTER", "UNDO"}

    radius: bpy.props.IntProperty(
        name="Radius",
        description="radius of the coral",
        default = 20)
    
    fringes: bpy.props.IntProperty(
        name="Fringes",
        description="fringes of the coral",
        default = 30)

    def execute(self, context):
        brainCoral(context, self.radius, self.fringes)
        return {'FINISHED'}

class simpleTableCoral(bpy.types.Operator):
    # MAIN
    bl_idname = "object.simple_table_coral"
    bl_label = "Simple Table Coral"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        tableCoral(context)
        return {'FINISHED'}

class simpleAntlerCoral(bpy.types.Operator):
    # MAIN
    bl_idname = "object.simple_antler_coral"
    bl_label = "Simple Antler Coral"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        antlerCoral(context)
        return {'FINISHED'}
   
class CoralPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Coral Panel"
    bl_idname = "OBJECT_PT_coral"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Coral Generator"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()
        row.operator(simpleBrainCoral.bl_idname, text="Brain Coral Generate", icon="SPHERE")

        row = layout.row()
        row.operator(simpleTableCoral.bl_idname, text="Table Coral Generate", icon="SPHERE")

        row = layout.row()
        row.operator(simpleAntlerCoral.bl_idname, text="Antler Coral Generate", icon="SPHERE")

        # Customize Properties of Brain Coral 
        # row = layout.row()
        # row.prop(simpleBrainCoral.bl_idname, 'radius')
        # row.prop(simpleBrainCoral.bl_idname, 'fringes',)
        

_classes = [
    simpleBrainCoral,
    simpleTableCoral,
    simpleAntlerCoral,
    CoralPanel
]

#register, unregister = bpy.utils.register_classes_factory(classes)

def register():
    for cls in _classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in _classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
