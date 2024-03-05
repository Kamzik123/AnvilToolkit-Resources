bl_info = {
    "name": "Remove unused Vertex Groups",
    "author": "CoDEmanX",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Properties Editor > Object data > Vertex Groups > Specials menu",
    "description": "Delete Vertex Groups with no assigned weight of active object",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh"}
 
 
import bpy
from bpy.types import Operator
 
 
class OBJECT_OT_vertex_group_remove_unused(Operator):
    bl_idname = "object.vertex_group_remove_unused"
    bl_label = "Remove unused Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}
    bl_region_type = 'UI'
 
    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH')

    def execute(self, context):

        ob = context.object
        ob.update_from_editmode()
       
        vgroup_used = {i: False for i, k in enumerate(ob.vertex_groups)}
       
        for v in ob.data.vertices:
            for g in v.groups:
                if g.weight > 0.0:
                    vgroup_used[g.group] = True
       
        for i, used in sorted(vgroup_used.items(), reverse=True):
            if not used:
                ob.vertex_groups.remove(ob.vertex_groups[i])
               
        return {'FINISHED'}

def draw_func(self, context):
    self.layout.operator(
    OBJECT_OT_vertex_group_remove_unused.bl_idname,
    icon='X')


classes = (
    OBJECT_OT_vertex_group_remove_unused,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.MESH_MT_vertex_group_context_menu.prepend(draw_func)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    bpy.types.MESH_MT_vertex_group_context_menu.remove(draw_func)
 
if __name__ == "__main__":
    register()