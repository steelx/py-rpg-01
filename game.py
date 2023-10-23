from typing import Optional

import pygame.display
from pygame.sprite import Group, Sprite
from pytmx import TiledMap
from pytmx.util_pygame import load_pygame

from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from sprite_objects import Tile, Circle, Rectangle


class Game:
    tmx_map: TiledMap
    map_group: Group
    entity_group: Group
    collision_group: Group
    foreground_group: Group
    foreground_objects: Group
    floor_objects: Group
    cam_x: float
    cam_y: float
    follow: Sprite = None

    def __init__(self, map_file: str, debug=False):
        self.tmx_map = load_pygame(map_file)
        self.width_pixel = self.tmx_map.width * self.tmx_map.tilewidth
        self.height_pixel = self.tmx_map.height * self.tmx_map.tileheight
        # Top left corner of the Camera in pixels
        self.cam_x = 0
        self.cam_y = 0

        self.display_surface = pygame.display.get_surface()
        self.map_group = CameraGroup()
        self.entity_group = CameraGroup()
        self.collision_group = CameraGroup()
        self.foreground_group = CameraGroup()
        self.foreground_objects = CameraGroup()
        self.floor_objects = CameraGroup()
        self.show_shapes = debug
        self.offset = pygame.math.Vector2()

    def setup(self):
        layer = self.tmx_map.get_layer_by_name('Floor')
        for x, y, image in layer.tiles():
            Tile((x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight), image, self.map_group)

        layer = self.tmx_map.get_layer_by_name('Foreground')
        for x, y, image in layer.tiles():
            Tile((x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight), image, self.foreground_group)

        # Collisions
        layer = self.tmx_map.get_layer_by_name('Collisions')
        for x, y, image in layer.tiles():
            Tile((x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight), image, self.collision_group, 50)

        # Process objects
        for obj in self.tmx_map.objects:
            if obj.image and obj.type == 'ForegroundItems':
                Tile((obj.x, obj.y), obj.image, self.foreground_objects)
            if obj.image and obj.type == 'FloorItems':
                Tile((obj.x, obj.y), obj.image, self.floor_objects)
            if obj.type == 'Marker' and self.show_shapes:
                spawn = (obj.x, obj.y)
                Circle(spawn, 4, 'yellow', self.map_group)
            if obj.type == 'Shape' and self.show_shapes:
                Rectangle((obj.x, obj.y), obj.width, obj.height, 'red', self.map_group)

    def update(self):
        if self.follow is not None:
            self.follow_entity()
        self.map_group.update()
        self.entity_group.update()
        self.foreground_group.update()

    def render(self):
        # Note that the order of rendering is important

        if hasattr(self.map_group, 'custom_draw'):
            self.map_group.custom_draw(self.cam_x, self.cam_y)
        if hasattr(self.floor_objects, 'custom_draw'):
            self.floor_objects.custom_draw(self.cam_x, self.cam_y)
        if hasattr(self.entity_group, 'custom_draw'):
            self.entity_group.custom_draw(self.cam_x, self.cam_y)
        if hasattr(self.foreground_group, 'custom_draw'):
            self.foreground_group.custom_draw(self.cam_x, self.cam_y)
        if hasattr(self.foreground_objects, 'custom_draw'):
            self.foreground_objects.custom_draw(self.cam_x, self.cam_y)
        if hasattr(self.collision_group, 'custom_draw'):
            self.collision_group.custom_draw(self.cam_x, self.cam_y)

    @classmethod
    def get_follow_position(cls):
        return cls.follow.rect.center

    def go_to(self, x: int, y: int):
        self.cam_x = x - SCREEN_WIDTH // 2
        self.cam_y = y - SCREEN_HEIGHT // 2
        # print(f"Top left corner of the map in pixels x, y: {self.cam_x}, {self.cam_y}")

    def _get_tile_pixel_cords(self, tile_x: int, tile_y: int):
        return (
            tile_x * self.tmx_map.tilewidth + self.tmx_map.tilewidth / 2,
            tile_y * self.tmx_map.tileheight + self.tmx_map.tileheight / 2
        )

    def go_to_tile(self, tile_x: int, tile_y: int):
        x, y = self._get_tile_pixel_cords(tile_x, tile_y)
        self.go_to(x, y)

    def pixel_to_tile(self, x: float, y: float) -> tuple[int, int]:
        """
        Convert absolute pixel coordinates to tile coordinates.
        :param x: x position in pixels
        :param y: y position in pixels
        :return: tilemap coordinates from a given x,y position
        """
        tile_x = x // self.tmx_map.tilewidth
        tile_y = (y // self.tmx_map.tileheight) - 1
        return tile_x, tile_y

    def point_to_tile(
            self, x: int, y: int
    ) -> tuple[int, int]:
        """
        Convert screen coordinates to tile coordinates.
        :param x: x position on the screen resolution
        :param y: y position on the screen resolution
        :return: tilemap coordinates from a given x,y position
        """
        # Calculate tile coordinates based on the adjusted position.
        x += self.cam_x
        y += self.cam_y

        # Adjust for the fact that the top-left corner of the map is at (0, 0).
        x = max(0, x)
        y = max(0, y)

        tile_size = self.tmx_map.tilewidth
        map_width = self.tmx_map.width
        map_height = self.tmx_map.height

        # Calculate tile coordinates based on the adjusted position.
        tile_x = x // tile_size
        tile_y = y // tile_size

        # Ensure that the tile coordinates are within the map bounds.
        tile_x = min(tile_x, map_width - 1)
        tile_y = min(tile_y, map_height - 1)

        return tile_x, tile_y

    def follow_entity(self):
        pos = self.follow.rect.center
        self.go_to(pos[0], pos[1])

    def get_tile(self, x: int, y: int, layer=0):
        return self.tmx_map.get_tile_image(x, y, layer)

    def get_tile_foot(self, tile_x: int, tile_y: int, height_modifier: int = 0):
        x, y = self._get_tile_pixel_cords(tile_x, tile_y)
        return x, y - height_modifier

    def get_blocking_tile(self, x: int, y: int) -> Optional[Tile]:
        """
        Get the Tile from the 'Collisions' layer that would block movement at the given tile coordinates.
        :param x: Tile X coordinate
        :param y: Tile Y coordinate
        :return: The blocking Tile, or None if there is no blocking Tile.
        """
        collisions_layer = self.tmx_map.get_layer_by_name('Collisions')
        for tile in collisions_layer.tiles():
            if tile[0] == x and tile[1] == y:
                return tile
        return None


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, cam_x, cam_y):
        self.offset.x = cam_x
        self.offset.y = cam_y

        # no sorted for now since it's causing a bug with the player in tweening
        # Sort sprites by their bottom position
        # sorted_sprites = sorted(self.sprites(), key=lambda s: s.rect.bottomright[1])

        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

