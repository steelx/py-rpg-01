from typing import Optional, Dict, Callable

import pygame.display
from pygame.sprite import Group, Sprite
from pytmx import TiledMap
from pytmx.util_pygame import load_pygame


from map_definitions import MapDefinition, Trigger, create_map_triggers
from map_utils import Camera, CameraGroup
from sprite_objects import Tile, Circle, Rectangle


class Game:
    tmx_map: TiledMap = None
    map_group: Group
    entity_group: Group
    collision_group: Group
    foreground_group: Group
    background_group: Group
    foreground_objects: Group
    floor_objects: Group
    cam_x: float
    cam_y: float
    follow: Sprite = None
    dt: float = 0

    def __init__(self, display: pygame.Surface = None, debug=False):
        """
        :type triggers: dict[str, Trigger] e.g. {'11,3': Trigger(ActionDef(on_enter=up_door_teleport))}
        :param display: pygame.Surface
        :param debug: bool
        """
        self.camera: Camera = None

        self.display_surface = display if display is not None else pygame.display.get_surface()
        self.map_group = CameraGroup(self.display_surface)
        self.entity_group = CameraGroup(self.display_surface)
        self.collision_group = CameraGroup(self.display_surface)
        self.foreground_group = CameraGroup(self.display_surface)
        self.background_group = CameraGroup(self.display_surface)
        self.foreground_objects = CameraGroup(self.display_surface)
        self.floor_objects = CameraGroup(self.display_surface)
        self.show_shapes = debug
        self.offset = pygame.math.Vector2()
        self.triggers = None
        self.triggers_type = None
        from character import Character
        self.npcs: list[Character] = []

    def setup(self, map_def: MapDefinition, actions: Dict[str, Callable] = None):
        self.tmx_map = load_pygame(map_def.path)
        width_pixel = self.tmx_map.width * self.tmx_map.tilewidth
        height_pixel = self.tmx_map.height * self.tmx_map.tileheight
        self.camera = Camera(self, width_pixel, height_pixel)

        if map_def.on_wake is not None:
            for v in map_def.on_wake:
                assert v.id in actions, f"Action {v.id} not found in ACTIONS"
                action = actions[v.id]
                action(self, **v.params)(None, None)

        # Create the Trigger types from the map_def
        self.triggers: Dict[str, Trigger] = create_map_triggers(map_def, actions, self)

        layer_map = {
            'Floor': self.map_group,
            'Foreground': self.foreground_group,
            'Background': self.background_group,
            'Collisions': self.collision_group
        }

        # Iterate over layers and create tiles
        for layer_name, group in layer_map.items():
            layer = self.tmx_map.get_layer_by_name(layer_name)
            for x, y, image in layer.tiles():
                pos = (x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight)
                Tile(pos, image, group, 0 if layer_name == 'Collisions' else None)

        # Process objects
        for obj in self.tmx_map.objects:
            if obj.image:
                if obj.type == 'ForegroundItems':
                    Tile((obj.x, obj.y), obj.image, self.foreground_objects)
                elif obj.type == 'FloorItems':
                    Tile((obj.x, obj.y), obj.image, self.floor_objects)

            if obj.type == 'Marker' and self.show_shapes:
                spawn = (obj.x, obj.y)
                Circle(spawn, 4, 'yellow', self.map_group)
            if obj.type == 'Shape' and self.show_shapes:
                Rectangle((obj.x, obj.y), obj.width,
                          obj.height, 'red', self.map_group)

    def update(self):
        if self.camera.follow is not None:
            self.camera.follow_entity()
        self.map_group.update()
        self.entity_group.update(game=self)
        self.foreground_group.update()
        for npc in self.npcs:
            npc.controller.update(self.dt)

    def render(self):
        cam_x, cam_y = self.camera.get_position()
        # Note that the order of rendering is important
        if hasattr(self.map_group, 'custom_draw'):
            self.map_group.custom_draw(cam_x, cam_y)
        if hasattr(self.floor_objects, 'custom_draw'):
            self.floor_objects.custom_draw(cam_x, cam_y)
        if hasattr(self.background_group, 'custom_draw'):
            self.background_group.custom_draw(cam_x, cam_y)
        if hasattr(self.entity_group, 'custom_draw'):
            self.entity_group.custom_draw(cam_x, cam_y, sort=True)
        if hasattr(self.foreground_group, 'custom_draw'):
            self.foreground_group.custom_draw(cam_x, cam_y)
        if hasattr(self.foreground_objects, 'custom_draw'):
            self.foreground_objects.custom_draw(cam_x, cam_y)
        if hasattr(self.collision_group, 'custom_draw'):
            self.collision_group.custom_draw(cam_x, cam_y)

    def _get_tile_pixel_cords(self, tile_x: int, tile_y: int):
        return (
            tile_x * self.tmx_map.tilewidth + self.tmx_map.tilewidth / 2,
            tile_y * self.tmx_map.tileheight + self.tmx_map.tileheight / 2
        )

    def go_to_tile(self, tile_x: int, tile_y: int):
        x, y = self._get_tile_pixel_cords(tile_x, tile_y)
        self.camera.go_to(x, y)

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

    def get_trigger_at_tile(self, tile_x: int, tile_y: int, layer="Floor"):
        """
        Get the Trigger at the given tile coordinates.
        :param tile_x: Tile X coordinate
        :param tile_y: Tile Y coordinate
        :param layer: Layer name to search for Triggers
        :return: The Trigger, or None if there is no Trigger at the given tile coordinates.
        """
        if self.triggers is None:
            return None
        tile_pos = f"{tile_x},{tile_y}"
        return self.triggers.get(tile_pos)

    def get_tile_foot(self, tile_x: int, tile_y: int, height_modifier: int = 0):
        x, y = self._get_tile_pixel_cords(tile_x, tile_y)
        return x, y - height_modifier

    def get_blocking_tile(self, tile_x: int, tile_y: int) -> Optional[Tile]:
        """
        Get the Tile from the 'Collisions' layer that would block movement at the given tile coordinates.
        :param tile_x: Tile X coordinate
        :param tile_y: Tile Y coordinate
        :return: The blocking Tile, or None if there is no blocking Tile.
        """
        collisions_layer = self.tmx_map.get_layer_by_name('Collisions')
        for tile in collisions_layer.tiles():
            if tile[0] == tile_x and tile[1] == tile_y:
                return tile
        return None

    def get_blocking_entity_tile(self, tile_x: int, tile_y: int) -> Optional[Tile]:
        """
        Get the Entity from the 'entity_group' group that would block movement at the given tile coordinates.
        :param tile_x: x position on the screen resolution
        :param tile_y: y position on the screen resolution
        :return: The blocking Tile, or None if there is no blocking Tile.
        """
        for entity in self.entity_group.sprites():
            if entity.tile_x == tile_x and entity.tile_y == tile_y:
                return entity
        return None

