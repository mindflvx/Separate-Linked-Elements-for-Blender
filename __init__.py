# SEPARATE LINKED ELEMENENTS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>. 

bl_info = {
    "name": "Separate Linked Elements",
    "author": "mindflux",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "Object menu > Separate Linked Elements",
    "description": "Separate linked elemenents of an object and places them into a new collection.",
    "warning": "",
    "wiki_url": "",
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
