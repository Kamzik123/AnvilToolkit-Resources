bl_info = {
    "name": "Convert vertex color to UV",
    "author": "Kamzik123",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "Properties Editor > Object data > Vertex Colors > Specials menu",
    "description": "Converts the active vertex color to UVs, overriding the active UV layer.",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh"}

import bpy
import mathutils
from bpy.types import Operator

class OBJECT_OT_vertex_color_convert_to_uv(Operator):
    bl_idname = "object.vertex_color_convert_to_uv"
    bl_label = "Convert color to UV"
    bl_options = {'REGISTER', 'UNDO'}
    bl_region_type = 'UI'
 
    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH')

    def execute(self, context):
        obj = context.object
        mesh = obj.data
        uv_coords = mesh.uv_layers[0]
        color_layer = mesh.attributes.active_color

        for poly in mesh.polygons:
            for li in poly.loop_indices:
                vi = mesh.loops[li].vertex_index
                color = color_layer.data[vi].color
                mesh.uv_layers.active.uv[li].vector = mathutils.Vector((color[0], color[1]))
               
        return {'FINISHED'}

def draw_func(self, context):
    self.layout.operator(
    OBJECT_OT_vertex_color_convert_to_uv.bl_idname)

classes = (
    OBJECT_OT_vertex_color_convert_to_uv,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.MESH_MT_color_attribute_context_menu.prepend(draw_func)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    bpy.types.MESH_MT_color_attribute_context_menu.remove(draw_func)
 
if __name__ == "__main__":
    register()