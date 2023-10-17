import pygame
from pygame.sprite import Group
from pytmx import TiledMap
from pytmx.util_pygame import load_pygame

from sprite_objects import Tile, Circle, Rectangle


def load_tmx_map(map_file) -> TiledMap:
    tmx = load_pygame(map_file)
    return tmx


def build_tiled_map(tmx_map: TiledMap, map_group: Group, shapes_group: Group = None):
    # all layers
    for layer in tmx_map.visible_layers:
        if hasattr(layer, "data"):
            for x, y, image in layer.tiles():
                Tile((x * tmx_map.tilewidth, y * tmx_map.tileheight), image, map_group)

    # objects
    for obj in tmx_map.objects:
        if obj.image and obj.type in ['Tree', 'Room']:
            Tile((obj.x, obj.y), obj.image, map_group)
        if obj.type == 'Marker':
            spawn = (obj.x, obj.y)
            Circle(spawn, 4, 'yellow', shapes_group)
        if obj.type == 'Shape':
            # TODO: shapes are not visible
            Rectangle((obj.x, obj.y), obj.width, obj.height, 'red', shapes_group)


def point_to_tile(
        x: int, y: int, tile_size: int, map_width: int, map_height: int
) -> tuple[int, int]:
    # Adjust for the fact that the top-left corner of the map is at (0, 0).
    x = max(0, x)
    y = max(0, y)

    # Calculate tile coordinates based on the adjusted position.
    tile_x = x // tile_size
    tile_y = y // tile_size

    # Ensure that the tile coordinates are within the map bounds.
    tile_x = min(tile_x, map_width - 1)
    tile_y = min(tile_y, map_height - 1)

    return tile_x, tile_y
