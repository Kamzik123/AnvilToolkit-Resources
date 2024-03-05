import bpy
import mathutils

#Scale a 2D vector v, considering a scale s and a pivot point p
def Scale2D( v, s, p ):
    return mathutils.Vector(( p.x + s.x*(v.x - p.x), p.y + s.y*(v.y - p.y)))

for obj in bpy.data.collections["Eyelashes_Collection"].objects:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.uv.pack_islands(udim_source='CLOSEST_UDIM', rotate=False, rotate_method='ANY', scale=True, merge_overlap=False, margin_method='SCALED', margin=0.0, pin=False, pin_method='LOCKED', shape_method='CONCAVE')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    uv_coords = obj.data.uv_layers.active
    up = 0
    down = 1
    left = 1
    right = 0
    for coord in uv_coords.uv:
        if coord.vector.x < left:
            left = coord.vector.x
        if coord.vector.x > right:
            right = coord.vector.x
        if coord.vector.y < down:
            down = coord.vector.y
        if coord.vector.y > up:
            up = coord.vector.y
    xsize = right - left
    ysize = up - down
    xfactor = 1 / xsize
    yfactor = 1 / ysize
    scale = mathutils.Vector((xfactor, yfactor))
    pos = mathutils.Vector((-left, -down))
    pivot = mathutils.Vector((0, 0))
    for coord in uv_coords.uv:
        coord.vector += pos
        coord.vector = Scale2D(coord.vector, scale, pivot)