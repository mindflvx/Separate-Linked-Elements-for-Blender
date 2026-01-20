import bpy
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty

class OBJECT_OT_separate_linked_elements(Operator):
    """Separate linked elements and place them in a new collection"""
    bl_idname = "object.separate_linked_elements"
    bl_label = "Separate Linked Elements"
    bl_options = {'REGISTER', 'UNDO'}

    collection_name: StringProperty(
        name="Collection Name",
        description="Name for the new collection",
        default="Separated Elements"
    )
    
    keep_original: BoolProperty(
        name="Keep Original",
        description="Keep the original object",
        default=False
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        original_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not original_objects:
            self.report({'WARNING'}, "No mesh objects selected")
            return {'CANCELLED'}

        # Create new collection
        new_collection = bpy.data.collections.new(self.collection_name)
        context.scene.collection.children.link(new_collection)

        separated_count = 0

        for obj in original_objects:
            # Store original object name
            original_name = obj.name
            
            # Make object active and deselect all
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj

            # Enter edit mode
            bpy.ops.object.mode_set(mode='EDIT')
            
            # Select all mesh elements
            bpy.ops.mesh.select_all(action='SELECT')
            
            # Separate by loose parts
            bpy.ops.mesh.separate(type='LOOSE')
            
            # Return to object mode
            bpy.ops.object.mode_set(mode='OBJECT')

            # Get all selected objects after separation
            selected_after_separate = list(context.selected_objects)
            
            # Check if separation actually occurred
            if len(selected_after_separate) == 1 and selected_after_separate[0] == obj:
                # No separation occurred (single element) - move original to new collection
                for col in obj.users_collection:
                    col.objects.unlink(obj)
                new_collection.objects.link(obj)
                separated_count += 1
            else:
                # Separation occurred - process all parts
                for sep_obj in selected_after_separate:
                    # Unlink from all collections
                    for col in sep_obj.users_collection:
                        col.objects.unlink(sep_obj)
                    
                    # Link to new collection
                    new_collection.objects.link(sep_obj)
                    separated_count += 1
                
                # Remove original if keep_original is False and it still exists
                if not self.keep_original and obj.name in bpy.data.objects:
                    bpy.data.objects.remove(obj, do_unlink=True)

        # Restore selection
        bpy.ops.object.select_all(action='DESELECT')
        for obj in new_collection.objects:
            obj.select_set(True)
        
        if new_collection.objects:
            context.view_layer.objects.active = new_collection.objects[0]

        self.report({'INFO'}, f"Separated {separated_count} elements into '{self.collection_name}'")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

def register():
    bpy.utils.register_class(OBJECT_OT_separate_linked_elements)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_separate_linked_elements)

