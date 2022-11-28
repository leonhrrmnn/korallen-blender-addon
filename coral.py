import bpy
import bmesh
import math
import mathutils
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


def addCoral():
    #TODO MAIN
    coral = 1

    
def addMenu(self, context):
    self.layout.operator(addCoral.bl_idname,
                         text="Add Coral")
    
#register, unregister = bpy.utils.register_classes_factory(classes)
def register():
    bpy.utils.register_class(Params)
    bpy.utils.register_class(addCoral)
    bpy.types.VIEW3D_MT_mesh_add.append(addMenu)


def unregister():
    bpy.utils.unregister_class(Params)
    bpy.utils.unregister_class(addCoral)
    bpy.types.VIEW3D_MT_mesh_add.remove(addMenu)
