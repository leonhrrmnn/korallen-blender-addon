import bpy
import bmesh
import mathutils
import math
from math import radians



bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge()

lSysCoral = bpy.ops.mesh.primitive_cone_add()
bpy.data.objects["Cone"].name = "LCoral_Obj"
bpy.data.meshes["Cone"].name = "LCoral_mesh"
lSysCoral = bpy.context.active_object
lSysCoral_nodes = lSysCoral.modifiers.new("LCoralNodes","NODES")
newSys = bpy.ops.node.new_geometry_node_group_assign()
bpy.data.node_groups["Geometry Nodes"].name = "LSysCoral_GeoNodes"
#newSys.name = "was"
lSysCoral_nodes.node_group = bpy.data.node_groups['LSysCoral_GeoNodes']
bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.clear()
#bpy.data.node_groups['LSysCorals_GeoNodes'].
# bpy.ops.node.tree_socket_add(in_out='IN')



coral_output = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('NodeGroupOutput')
Input1 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('NodeGroupInput')
Input2 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('NodeGroupInput')
Input3 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('NodeGroupInput')
Baseline = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCurvePrimitiveLine')
Baseline.mode = 'DIRECTION'

Basecurve = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeResampleCurve')
Basecurve.inputs[2].default_value = 30
Baseline.inputs[3].default_value = 3
SetPos = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeSetPosition')
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Baseline.outputs[0], Basecurve.inputs[0])

bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Input1.outputs[1], Baseline.inputs[3])

pattern = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeTexNoise')
BasePatternRange = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMapRange')
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(pattern.outputs[0], BasePatternRange.inputs[0])

#bpy.data.node.tree_socket_add(in_out='IN')


minConvert = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMath')
minConvert.operation = 'MULTIPLY'
minConvert.inputs[1].default_value = -1

bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(minConvert.outputs[0], BasePatternRange.inputs[3])
capAtri = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCaptureAttribute')
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Basecurve.outputs[0], capAtri.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(capAtri.outputs[0], SetPos.inputs[0])
spline = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeSplineParameter')
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(spline.outputs[0], capAtri.inputs[1])

BasePatternRange2 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMapRange')
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(spline.outputs[0], capAtri.inputs[2])
#bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Input2.outputs[2], BasePatternRange2.inputs[4])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(BasePatternRange2.outputs[0], minConvert.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(BasePatternRange2.outputs[0], BasePatternRange.inputs[4])

combine_xy = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeCombineXYZ')
BasePatternRange3 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMapRange')
pattern2 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeTexNoise')
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(BasePatternRange.outputs[0], combine_xy.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(pattern2.outputs[0], BasePatternRange3.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(combine_xy.outputs[0], SetPos.inputs[3])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(BasePatternRange3.outputs[0], combine_xy.inputs[1])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(minConvert.outputs[0], BasePatternRange3.inputs[3])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(BasePatternRange2.outputs[0], BasePatternRange3.inputs[4])

trimmer = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeTrimCurve')
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(SetPos.outputs[0], trimmer.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(trimmer.outputs[0], coral_output.inputs[0])



BasePatternRange4 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMapRange')

bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(BasePatternRange4.outputs[0], BasePatternRange2.inputs[4])

capAtri2 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCaptureAttribute')
spline2 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeSplineParameter')
MapRange = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMapRange')
radius = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeSetCurveRadius')
circle = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCurvePrimitiveCircle')
c2m = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCurveToMesh')
curve_graph = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeFloatCurve')

bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(SetPos.outputs[0], trimmer.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(trimmer.outputs[0], capAtri2.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(spline2.outputs[0], capAtri2.inputs[2])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(capAtri2.outputs[0], radius.inputs[0])
#bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(capAtri2.outputs[1], MapRange.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(MapRange.outputs[0], curve_graph.inputs[1])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(curve_graph.outputs[0], radius.inputs[2])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(radius.outputs[0], c2m.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(circle.outputs[0], c2m.inputs[1])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(capAtri.outputs[1], BasePatternRange2.inputs[0])
MapRange.inputs[3].default_value = 1
MapRange.inputs[4].default_value = 0



multiplay = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMath')
multiplay.operation = 'MULTIPLY'

bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(circle.inputs[4], multiplay.outputs[0])


points = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeInstanceOnPoints')
cLine = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCurvePrimitiveLine')
join = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeJoinGeometry')
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(points.inputs[0], capAtri2.outputs[0])



#importante part here
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(capAtri2.outputs[2], MapRange.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(cLine.outputs[0], points.inputs[2])
cLine.inputs[1].default_value[2] = 3.5
#bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(points.outputs[0], join.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(c2m.outputs[0], join.inputs[0])

points.inputs[5].default_value[1] = radians(69)
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(curve_graph.outputs[0], points.inputs[6])

tangent = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeInputTangent')
branch_rotation = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeCombineXYZ')
branch_rotation.inputs[1].default_value = 8
rot_to_vektor = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('FunctionNodeAlignEulerToVector')
rot_branches = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeRotateInstances')


bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(points.outputs[0], rot_branches.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(tangent.outputs[0], rot_to_vektor.inputs[2])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(branch_rotation.outputs[0], rot_to_vektor.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(rot_to_vektor.outputs[0], points.inputs[5])
rot_branches.inputs[2].default_value[1] = radians(69)

bc2m = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCurveToMesh')
bcircle = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCurvePrimitiveCircle')
Input4 = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('NodeGroupInput')
slim = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMath')
bradius = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeSetCurveRadius')
bMapRange = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeMapRange')
bcapAtri = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeCaptureAttribute')
bspline = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeSplineParameter')
bcurve_graph = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('ShaderNodeFloatCurve')

slim.operation = 'MULTIPLY'
bcircle.inputs[0].default_value = 10
bcircle.inputs[4].default_value = 0.05
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(rot_branches.outputs[0], bcapAtri.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bradius.outputs[0], bc2m.inputs[0])

bMapRange.inputs[3].default_value = 1
bMapRange.inputs[4].default_value = 0
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bc2m.outputs[0], join.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bcircle.outputs[0], bc2m.inputs[1])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(slim.outputs[0], bcircle.inputs[4])

bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bcapAtri.outputs[0], bradius.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bspline.outputs[0], bcapAtri.inputs[2])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bcapAtri.outputs[2], bMapRange.inputs[2])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bMapRange.outputs[0], bcurve_graph.inputs[1])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(bcurve_graph.outputs[0], bradius.inputs[2])

Texture = bpy.data.node_groups['LSysCoral_GeoNodes'].nodes.new('GeometryNodeSetMaterial')

bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(join.outputs[0], Texture.inputs[0])
bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(Texture.outputs[0], coral_output.inputs[0])

cTexture = bpy.data.materials.new(name= "Korallse")
cTexture.use_nodes = True
#bpy.data.node_groups['LSysCoral_GeoNodes'].links.new(transform_coral2.outputs[0], combine.inputs[0])

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

Texture.inputs[2].default_value = cTexture

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
