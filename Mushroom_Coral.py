import bpy
import bmesh
import mathutils
import math
from math import radians



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
#coral1.values()

#bpy.data.node_groups['Coral1_GeoNodes'].nodes
#coral_output.output[0] = none

#coral_base.inputs.new()
#coral_base.inputs[0] = combine.outputs[0]
#combine.inputs[0] = coral_base.outputs[0]

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

#bpy.context.object.color = object_color
#nodes["Join Geometry"].inputs[0].default_value = object_color 

#cone1 = coral_nodes.node.new(type="GeometryMeshNodeCone")
#cone1.node_group = bpy.data.node_groups['Coral1_GeoNodes']

#coral_nodes.node_group = bpy.data.node_groups['CoralNodes']

#bpy.ops.object.modifier_add(type='NODES')
#bpy.ops.node.new_geometry_node_group_assign()
#bpy.data.node_groups["Geometry Nodes.001"].name = "Coral1"
#gnode = bpy.data.node_groups["Coral1"]

#cone_base = bpy.ops.node.add_node(type="GeometryMeshNodeCone")

#gnode.node_tree.nodes.new("Join Geometry")

join = bpy.data


coral1_mesh = bpy.data.meshes.new("coral1_mesh")
coral1_object = bpy.data.objects.new("coral1_object", coral1_mesh)


bpy.context.collection.objects.link(coral1_object)
bpy.ops.transform.rotate(value = 0.1)

bm = bmesh.new()
bm.from_mesh(coral1_mesh)
  

bm.to_mesh(coral1_mesh)
bm.free()

