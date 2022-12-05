import bpy
import math

RADIUS = 20

# Szene leeren
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge()

bpy.ops.mesh.primitive_circle_add(radius=RADIUS, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

curmesh = bpy.context.object.data

for vert in curmesh.vertices:
    
    if vert.co.z < vert.co.z / 2:
        
        x = 0
        y = 0
        
        vert.co.x = x
        vert.co.y = y
        vert.co.z = 0