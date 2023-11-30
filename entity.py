from dataclasses import dataclass
from typing import Dict

import pygame

from game import Game
from sprite_utils import load_sprite_sheet


@dataclass
class EntityDefinition:
    """
    Entity definition
    :param tile_x: tile x position
    :param tile_y: tile y position
    :param start_frame: start frame of the sprite
    :param height: height of the sprite png
    :param width: width of the sprite png
    :param texture_path: path to png sprite
    :param rows: rows of the spritesheet
    :param columns: columns of the spritesheet
    :param height_mod: height modifier
    """
    tile_x: int
    tile_y: int
    start_frame: int
    height: int
    width: int
    texture_path: str
    rows: int
    columns: int
    height_mod: int = 4


class Entity(pygame.sprite.Sprite):
    tile_x: int
    tile_y: int
    height_mod: int
    texture: pygame.Surface
    spritesheet: list[pygame.Surface]
    frame: int

    def __init__(self, entity_def: EntityDefinition, game: Game):
        super().__init__(game.entity_group)
        self.definition = entity_def
        self.tile_x = entity_def.tile_x
        self.tile_y = entity_def.tile_y
        self.frame = entity_def.start_frame
        self.height_mod = entity_def.height_mod
        pos = game.tmx_map.get_tile_foot(
            self.tile_x, self.tile_y, entity_def.height_mod)
        sprite_sheet = load_sprite_sheet(
            entity_def.texture_path, entity_def.width, entity_def.height, entity_def.rows, entity_def.columns)
        self.spritesheet = sprite_sheet
        self.image = sprite_sheet[self.frame]
        self.rect = self.image.get_rect(center=pos)
        self.visible = True  # used at explore_state to stop handling event
        self.children: Dict[str, Entity] = {}

    def add_child(self, id: str, entity: 'Entity'):
        self.children[id] = entity

    def remove_child(self, id: str):
        self.children.pop(id, None)

    def update(self, game: Game):
        self.tile_x, self.tile_y = game.tmx_map.pixel_to_tile(
            self.rect.midbottom[0], self.rect.midbottom[1])
        self.image = self.spritesheet[self.frame]

    def render(self, *args, **kwargs):
        pass

    def set_tile_pos(self, tile_x: int, tile_y: int, game: Game):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.rect.center = game.tmx_map.get_tile_foot(
            self.tile_x, self.tile_y, self.height_mod)

    def set_frame(self, start_frame: int):
        self.frame = start_frame
