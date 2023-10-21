from typing import Dict, Any

import pygame

from entity import Entity
from game import Game
from keyboard import TileMovementHandler
from statemachine import StateMachine


class WaitState:
    entity: Entity
    controller: StateMachine
    game_map: Game

    def __init__(self, character: Dict[str, Any], game_map: Game):
        self.character = character
        self.game_map = game_map
        self.entity = character["entity"]
        self.controller = character["controller"]
        self.frame_reset_speed = 0.05
        self.frame_count = 0
        self.keyboard = TileMovementHandler(800)

    def enter(self, **kwargs):
        # reset to default frame
        self.frame_count = 0
        self.entity.set_frame(self.entity.start_frame)

    def exit(self):
        pass

    def render(self, **kwargs):
        pass

    def update(self):
        if self.frame_count != -1:
            self.frame_count += pygame.time.get_ticks()
            if self.frame_count >= self.frame_reset_speed:
                self.frame_count = -1
                self.entity.set_frame(self.entity.start_frame)

        def change_state(dx, dy):
            if self.controller:
                self.controller.change("walk", dx=dx, dy=dy)
        self.keyboard.handle_input(change_state)
