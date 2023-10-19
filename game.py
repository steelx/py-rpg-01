import pygame.display
from pygame.sprite import Group
from pytmx import TiledMap
from pytmx.util_pygame import load_pygame

from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from sprite_objects import Tile, Circle, Rectangle, Entity


class Game:
    tmx_map: TiledMap
    map_group: Group
    shapes_group: Group = None
    cam_x: float
    cam_y: float
    follow: Entity = None

    def __init__(self, map_file: str, debug=False):
        self.tmx_map = load_pygame(map_file)
        self.width_pixel = self.tmx_map.width * self.tmx_map.tilewidth
        self.height_pixel = self.tmx_map.height * self.tmx_map.tileheight
        # Top left corner of the map in pixels
        self.cam_x = 0
        self.cam_y = 0

        self.display_surface = pygame.display.get_surface()
        self.map_group = CameraGroup()
        self.show_shapes = debug
        self.offset = pygame.math.Vector2()

    def setup(self):
        # Process all layers
        for layer in self.tmx_map.visible_layers:
            if hasattr(layer, "data"):
                for x, y, image in layer.tiles():
                    Tile((x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight), image, self.map_group)

        # Process objects
        for obj in self.tmx_map.objects:
            if obj.image and obj.type in ['Tree', 'Room']:
                Tile((obj.x, obj.y), obj.image, self.map_group)
            if obj.type == 'Marker' and self.show_shapes:
                spawn = (obj.x, obj.y)
                Circle(spawn, 4, 'yellow', self.map_group)
            if obj.type == 'Shape' and self.show_shapes:
                Rectangle((obj.x, obj.y), obj.width, obj.height, 'red', self.map_group)

    def update(self):
        self.map_group.update()

    def render(self):
        if hasattr(self.map_group, 'custom_draw'):
            self.map_group.custom_draw(self.cam_x, self.cam_y)

    @classmethod
    def get_follow_position(cls):
        return cls.follow.rect.center

    def go_to(self, x: int, y: int):
        self.cam_x = x - SCREEN_WIDTH // 2
        self.cam_y = y - SCREEN_HEIGHT // 2
        print(f"Top left corner of the map in pixels x, y: {self.cam_x}, {self.cam_y}")

    def go_to_tile(self, tile_x: int, tile_y: int):
        self.go_to(
            tile_x * self.tmx_map.tilewidth + self.tmx_map.tilewidth / 2,
            tile_y * self.tmx_map.tileheight + self.tmx_map.tileheight / 2
        )

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

    def get_tile(self, x: int, y: int, layer=0):
        return self.tmx_map.get_tile_image(x, y, layer)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, cam_x, cam_y):
        self.offset.x = cam_x
        self.offset.y = cam_y

        # Sort sprites by their vertical position
        def sort_sprite(s: pygame.sprite.Sprite):
            return s.rect.bottomright

        for sprite in sorted(self.sprites(), key=sort_sprite):
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)
