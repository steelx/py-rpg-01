from typing import Optional

from pytmx import load_pygame

from sprite_utils import Tile


class TmxMap:
    def __init__(self, map_pth: str):
        self.tiledmap = load_pygame(map_pth)

    def get_wh_pixels(self) -> tuple[int, int]:
        return self.tiledmap.width * self.tiledmap.tilewidth, self.tiledmap.height * self.tiledmap.tileheight

    def point_to_tile(self, x: int, y: int, camera_pos: tuple[float, float]) -> tuple[int, int]:
        """
        Convert screen coordinates to tile coordinates.
        :param x: x position on the screen resolution
        :param y: y position on the screen resolution
        :param camera_pos: game.camera.x, game.camera.y
        :return: tilemap coordinates from a given x,y position
        """
        # Calculate tile coordinates based on the adjusted position.
        x += camera_pos[0]
        y += camera_pos[1]

        # Adjust for the fact that the top-left corner of the map is at (0, 0).
        x = max(0, x)
        y = max(0, y)

        tile_size = self.tiledmap.tilewidth
        map_width = self.tiledmap.width
        map_height = self.tiledmap.height

        # Calculate tile coordinates based on the adjusted position.
        tile_x = x // tile_size
        tile_y = y // tile_size

        # Ensure that the tile coordinates are within the map bounds.
        tile_x = min(tile_x, map_width - 1)
        tile_y = min(tile_y, map_height - 1)
        return tile_x, tile_y

    def get_blocking_tile(self, tile_x: int, tile_y: int) -> Optional[Tile]:
        """
        Get the Tile from the 'Collisions' layer that would block movement at the given tile coordinates.
        :param tile_x: Tile X coordinate
        :param tile_y: Tile Y coordinate
        :return: The blocking Tile, or None if there is no blocking Tile.
        """
        collisions_layer = self.tiledmap.get_layer_by_name('Collisions')
        for tile in collisions_layer.tiles():
            if tile[0] == tile_x and tile[1] == tile_y:
                return tile
        return None

    def pixel_to_tile(self, x: float, y: float) -> tuple[int, int]:
        """
        Convert absolute pixel coordinates to tile coordinates.
        :param x: x position in pixels
        :param y: y position in pixels
        :return: tilemap coordinates from a given x,y position
        """
        tile_x = x // self.tiledmap.tilewidth
        tile_y = (y // self.tiledmap.tileheight) - 1
        return tile_x, tile_y

    def get_tile_foot(self, tile_x: int, tile_y: int, height_modifier: int = 0):
        x, y = self.get_tile_pixel_cords(tile_x, tile_y)
        return x, y - height_modifier

    def get_tile_pixel_cords(self, tile_x: int, tile_y: int):
        return (
            tile_x * self.tiledmap.tilewidth + self.tiledmap.tilewidth / 2,
            tile_y * self.tiledmap.tileheight + self.tiledmap.tileheight / 2
        )
