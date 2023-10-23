from typing import Dict, Any

import pygame

from entity import Entity
from game import Game
from statemachine import StateMachine


class WaitState:
    entity: Entity
    controller: StateMachine
    game: Game

    def __init__(self, character: Dict[str, Any], game: Game):
        self.character = character
        self.game = game
        self.entity = character["entity"]
        self.controller = character["controller"]
        self.frame_reset_speed = 17  # 17ms
        self.next_frame_time = 0

    def enter(self, **kwargs):
        # reset to default frame
        self.next_frame_time = pygame.time.get_ticks() + 80
        self.entity.set_frame(self.entity.definition.start_frame)

    def exit(self):
        pass

    def render(self, **kwargs):
        pass

    def update(self):
        self.reset_frame()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.change_state(-1, 0)
        elif keys[pygame.K_RIGHT]:
            self.change_state(1, 0)
        elif keys[pygame.K_UP]:
            self.change_state(0, -1)
        elif keys[pygame.K_DOWN]:
            self.change_state(0, 1)

    def change_state(self, dx, dy):
        if self.controller:
            self.controller.change("move", dx=dx, dy=dy)

    def reset_frame(self):
        """
        If we're in the wait state for a few frames, reset the frame to the default
        :return:
        """
        if self.entity.start_frame == self.entity.definition.start_frame:
            return
        current = pygame.time.get_ticks()
        if current > self.next_frame_time:
            self.next_frame_time = current + 80
            self.entity.set_frame(self.entity.definition.start_frame)
