import math
from typing import Dict, Any

import pygame

from animations import Animation
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
        self.move_speed = 0.5 * 1000  # 0.3 seconds
        self.tween = None
        self.anim = Animation([self.entity.start_frame])

    def enter(self, **kwargs):
        self.move_x = kwargs.get("dx", 0)
        self.move_y = kwargs.get("dy", 0)
        pixel_pos = self.entity.rect.center
        self.pixel_x = pixel_pos[0]
        self.pixel_y = pixel_pos[1]
        self.tween = Tween(0, self.tile_width, self.move_speed)
        self.tween.start()
        frames = []
        if self.move_x == -1:
            frames = self.character["anim"]["left"]
        elif self.move_x == 1:
            frames = self.character["anim"]["right"]
        elif self.move_y == -1:
            frames = self.character["anim"]["up"]
        elif self.move_y == 1:
            frames = self.character["anim"]["down"]
        self.anim.set_frames(frames)

        if self.game.get_blocking_tile(self.entity.tile_x + self.move_x, self.entity.tile_y + self.move_y):
            self.move_x = 0
            self.move_y = 0
            self.controller.change("wait")
            return

    def exit(self):
        # character finishes entering a tile. This occurs when
        # the character exits the MoveState
        trigger = self.game.get_trigger_at_tile(self.entity.tile_x, self.entity.tile_y)
        if trigger is not None:
            trigger.onEnter(None, self.entity)

    def render(self, **kwargs):
        pass

    def update(self):
        self.anim.update()
        self.tween.update()
        self.entity.set_frame(self.anim.frame())
        value = self.tween.value
        x = self.pixel_x + (self.move_x * value)
        y = self.pixel_y + (self.move_y * value)
        x = math.floor(x)
        y = math.floor(y)
        self.entity.rect.center = (x, y)

        if not self.tween.animating and self.anim.is_finished():
            self.controller.change("wait")