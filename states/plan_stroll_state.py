import random

from game import Game
from utils import CountdownTimer

WAIT_TIME_MS = 400


class PlanStrollState:
    def __init__(self, character, game: Game):
        from character import Character
        assert isinstance(
            character, Character), "Expected character to be an instance of Character"

        self.character = character
        self.game = game
        self.entity = character.entity
        self.controller = character.controller
        self.next_frame_timer = CountdownTimer(WAIT_TIME_MS)
        count_down = random.randint(1500, 4000)
        self.count_down_timer = CountdownTimer(count_down)

    def enter(self, **kwargs) -> None:
        self.next_frame_timer.reset()
        count_down = random.randint(1500, 4000)
        self.count_down_timer.reset(count_down)

    def exit(self) -> None:
        pass

    def render(self, **kwargs) -> None:
        pass

    def update(self, dt: float) -> None:
        self.change_direction()
        self.reset_frame()

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

    def change_direction(self):
        if self.count_down_timer.has_elapsed():
            choice = random.randint(0, 4)
            if choice == 0:
                self.controller.change("move", dx=-1, dy=0)
            elif choice == 1:
                self.controller.change("move", dx=1, dy=0)
            elif choice == 2:
                self.controller.change("move", dx=0, dy=-1)
            elif choice == 3:
                self.controller.change("move", dx=0, dy=1)
