from pytmx import TiledMap
from pytmx.util_pygame import load_pygame

def load_tmx_map(map_file) -> TiledMap:
    tmx_map = load_pygame(map_file)
    return tmx_map


tmx_map = load_tmx_map(PATH + 'cave/cave_map.tmx')

# get all layers as Dict
print(tmx_map.layernames)

# get Object Layers
for obj in tmx_map.objectgroups:
    print(obj.name)
    print(obj)

# get Tile Layers
layer = tmx_map.get_layer_by_name('Ground')
for x, y, surface in layer.tiles():
    print(x, y, surface)

# get Objects return a list of TiledObject
object_layer = tmx_map.get_layer_by_name('Objects')
for obj in object_layer:
    print(obj)

# or get objects by key
# (same as above but only in case if you 1 objects layer)
for obj in tmx_map.objects:
    print(obj.x, obj.y, obj.image)
    if obj.type == 'Tree':
        print("type Tree: " + obj.name)
    if obj.type == 'Marker':
        print("type Marker: " + obj.name)