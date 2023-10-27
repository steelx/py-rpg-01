import pygame

from entity import Entity
from game import Game
from statemachine import StateMachine
from utils.count_down_timer import CountdownTimer

WAIT_TIME_SECONDS = 0.3


class WaitState:
    entity: Entity
    controller: StateMachine
    game: Game

    def __init__(self, character, game: Game):
        from character import Character
        assert isinstance(
            character, Character), "Expected character to be an instance of Character"
        self.character = character
        self.game = game
        self.entity = character.entity
        self.controller = character.controller
        self.next_frame_timer = CountdownTimer(WAIT_TIME_SECONDS)

    def enter(self, **kwargs):
        self.next_frame_timer = CountdownTimer(WAIT_TIME_SECONDS)
        self.entity.set_frame(self.entity.frame)

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
        if self.entity.frame == self.entity.definition.start_frame:
            return
        if self.next_frame_timer.has_elapsed():
            self.entity.set_frame(self.entity.definition.start_frame)
            self.character.facing = "down"
