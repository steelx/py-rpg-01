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


## fonts
since I'm loading fonts via theme regular_path key not loading fonts via ui_manager.add_font_paths
ui_manager.add_font_paths("BigBlueTerm437NerdFontMono", str(ASSETS_PATH + "fonts/BigBlueTerm437NerdFontMono-Regular.ttf"))


### GUI
hero_tile_rect = game.get_scaled_rect_for_ui(9, 5)
health_bar = ProgressBar(
    rect=hero_tile_rect,
    manager=ui_manager,
    start_progress=10,
    object_id="@hp_progress_bar"
)
health_bar.set_progress(20)

stack.push(
    Selections(
        title="Select an action",
        options=["YES", "NO"],
        position=(50, 50),
        width=100,
        columns=1,
        manager=stack.manager
    )
)

stack.push(
    DialoguePanel(
        hero_image=hero_image_path,
        hero_name="Hero",
        message=message,
        manager=stack.manager
    )
)

stack.push(
    Textbox(message, (50, 100), (150, 100), chars_per_line=12, lines_per_chunk=3,
            manager=stack.manager)
)