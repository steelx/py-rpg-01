from dataclasses import dataclass

import pygame

from game import Game
from spritesheet import load_sprite_sheet


@dataclass
class CharacterDefinition:
    tile_x: int
    tile_y: int
    start_frame: int
    height: int
    width: int
    texture_path: str
    height_mod: int = 4


class Entity(pygame.sprite.Sprite):
    tile_x: int
    tile_y: int
    height_mod: int
    texture: pygame.Surface
    spritesheet: list[pygame.Surface]
    start_frame: int
    game: Game

    @classmethod
    def create(cls, character_def: CharacterDefinition, game: Game):
        cls.game = game
        cls.tile_x = character_def.tile_x
        cls.tile_y = character_def.tile_y
        cls.start_frame = character_def.start_frame
        cls.height_mod = character_def.height_mod
        pos = game.get_tile_foot(cls.tile_x, cls.tile_y, character_def.height_mod)
        # TODO: fix sprite rows columns
        sprite_sheet = load_sprite_sheet(character_def.texture_path, character_def.width, character_def.height, 9, 16)
        return cls(pos, sprite_sheet, game.map_group)

    def __init__(self, pos: tuple[float, float], spritesheet: list[pygame.Surface], group: pygame.sprite.Group):
        super().__init__(group)
        self.spritesheet = spritesheet
        self.image = spritesheet[self.start_frame]
        self.rect = self.image.get_rect(center=pos)

    def update(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        pass

    def teleport(self, move_x: int, move_y: int):
        self.tile_x += move_x
        self.tile_y += move_y
        self.rect.center = self.game.get_tile_foot(self.tile_x, self.tile_y, self.height_mod)
