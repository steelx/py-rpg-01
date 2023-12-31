from typing import Optional, Dict, Callable, Tuple

import pygame.display

from globals import NATURAL_SIZE
from map_definitions import MapDefinition, Trigger, create_map_triggers
from map_utils import Camera, CameraGroup, TmxMap
from sprite_utils import Tile, Circle, Rectangle
from world import World


class Game:
    world: World
    tmx_map: TmxMap = None
    map_group: CameraGroup
    entity_group: CameraGroup
    collision_group: CameraGroup
    foreground_group: CameraGroup
    background_group: CameraGroup
    foreground_objects: CameraGroup
    floor_objects: CameraGroup
    cam_x: float
    cam_y: float
    dt: float = 0

    def __init__(self, display: pygame.Surface = None, debug=False):
        """
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
        self.tmx_map = TmxMap(map_def.path)
        width_pixel, height_pixel = self.tmx_map.get_wh_pixels()
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
            layer = self.tmx_map.tiledmap.get_layer_by_name(layer_name)
            for x, y, image in layer.tiles():
                pos = (x * self.tmx_map.tiledmap.tilewidth, y * self.tmx_map.tiledmap.tileheight)
                Tile(pos, image, group, 0 if layer_name == 'Collisions' else None)

        # Process objects
        for obj in self.tmx_map.tiledmap.objects:
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

    def update(self, dt: float = None):
        dt = dt if dt is not None else self.dt
        self.world.update(dt)
        self.map_group.update()
        self.entity_group.update(game=self)
        for npc in self.npcs:
            npc.controller.update(dt)
        if self.camera.follow is not None:
            self.camera.follow_entity()

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

    def go_to_tile(self, tile_x: int, tile_y: int):
        x, y = self.tmx_map.get_tile_pixel_cords(tile_x, tile_y)
        self.camera.go_to(x, y)

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

    def get_tile_pos_for_ui(self, tile_x: int, tile_y: int, offset: pygame.Vector2 = None) -> Tuple[float, float]:
        # Calculate the top center of the hero, then move up by the height of the progress bar plus some padding
        offset = offset if offset is not None else pygame.Vector2()
        window_size = pygame.display.get_surface().get_size()
        scale_x = window_size[0] / NATURAL_SIZE[0]
        scale_y = window_size[1] / NATURAL_SIZE[1]
        pos = self.tmx_map.get_tile_pixel_cords(tile_x, tile_y)
        scaled_top_center_x = (pos[0] - self.camera.x) * scale_x
        scaled_top_center_y = (pos[1] - self.camera.y) * scale_y
        return scaled_top_center_x + offset.x, scaled_top_center_y + offset.y

    def get_hero_pos_for_ui(self, offset: pygame.Vector2 = None) -> Tuple[float, float]:
        # Calculate the top center of the hero, then move up by the height of the progress bar plus some padding
        offset = offset if offset is not None else pygame.Vector2()
        window_size = pygame.display.get_surface().get_size()
        scale_x = window_size[0] / NATURAL_SIZE[0]
        scale_y = window_size[1] / NATURAL_SIZE[1]
        tile_x, tile_y = self.camera.follow.tile_x, self.camera.follow.tile_y
        pos = self.tmx_map.get_tile_pixel_cords(tile_x, tile_y)
        scaled_top_center_x = (pos[0] - self.camera.x) * scale_x
        scaled_top_center_y = (pos[1] - self.camera.y) * scale_y
        return scaled_top_center_x + offset.x, scaled_top_center_y + offset.y
