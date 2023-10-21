import math
from typing import Dict, Any

import pygame

from entity import Entity
from game import Game
from statemachine import StateMachine
from tweener import Tween


class MoveState:
    entity: Entity
    controller: StateMachine
    game: Game

    def __init__(self, character: Dict[str, Any], game: Game):
        self.character = character
        self.game = game
        self.entity = character["entity"]
        self.controller = character["controller"]
        self.tile_width = game.tmx_map.tilewidth
        self.move_x = 0
        self.move_y = 0
        self.pixel_x = 0
        self.pixel_y = 0
        self.move_speed = 0.3
        self.tween = Tween(0, 0, 1)

    def enter(self, **kwargs):
        self.move_x = kwargs.get("dx", 0)
        self.move_y = kwargs.get("dy", 0)
        # print(f"MoveState: {self.move_x}, {self.move_y}")
        pixel_pos = self.entity.rect.center
        self.pixel_x = pixel_pos[0]
        self.pixel_y = pixel_pos[1]
        self.tween = Tween(0, self.tile_width, self.move_speed*1000)
        self.tween.start()

    def exit(self):
        self.entity.teleport(self.move_x, self.move_y, self.game)

    def render(self, **kwargs):
        pass

    def update(self):
        # elapsed_time = (pygame.time.get_ticks() % 1000) / 1000
        self.tween.update()
        value = self.tween.value
        x = self.pixel_x + (self.move_x * value)
        y = self.pixel_y + (self.move_y * value)
        x = math.floor(x)
        y = math.floor(y)
        self.entity.rect.center = (x, y)
        if not self.tween.animating:
            self.controller.change("wait")
