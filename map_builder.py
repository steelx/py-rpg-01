from pygame.sprite import Group
from pytmx import TiledMap
from pytmx.util_pygame import load_pygame

from sprite_objects import Tile, Circle, Rectangle


class MapBuilder:
    tmx_map: TiledMap

    def __init__(self, map_file: str):
        self.tmx_map = load_pygame(map_file)

    def build_map(self, map_group: Group, shapes_group: Group = None):
        # Process all layers
        for layer in self.tmx_map.visible_layers:
            if hasattr(layer, "data"):
                for x, y, image in layer.tiles():
                    Tile((x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight), image, map_group)

        # Process objects
        for obj in self.tmx_map.objects:
            if obj.image and obj.type in ['Tree', 'Room']:
                Tile((obj.x, obj.y), obj.image, map_group)
            if obj.type == 'Marker' and shapes_group is not None:
                spawn = (obj.x, obj.y)
                Circle(spawn, 4, 'yellow', shapes_group)
            if obj.type == 'Shape' and shapes_group is not None:
                Rectangle((obj.x, obj.y), obj.width, obj.height, 'red', shapes_group)

    def point_to_tile(
            self, x: int, y: int
    ) -> tuple[int, int]:
        """
        :return: tilemap coordinates from a given x,y position
        """
        tile_size = self.tmx_map.tilewidth
        map_width = self.tmx_map.width
        map_height = self.tmx_map.height
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
