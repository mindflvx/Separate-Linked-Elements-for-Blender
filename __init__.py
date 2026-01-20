bl_info = {
    "name": "Separate Linked Elements",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Object > Separate Linked Elements",
    "description": "Separates linked elements and places them in a new collection",
    "category": "Object",
}

import bpy
from . import operator

def menu_func(self, context):
    self.layout.operator(operator.OBJECT_OT_separate_linked_elements.bl_idname)

def register():
    operator.register()
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    operator.unregister()

if __name__ == "__main__":
    register()
