from typing import Callable

import pygame

from storyboard import Storyboard, Event, Wait
from storyboard.states import FadeState


def fade_screen(alpha: int, duration: float, renderer: pygame.Surface) -> Callable[[Storyboard], Event]:
    def create_event(storyboard: Storyboard) -> Event:
        state = FadeState(params={"alpha_start": 255, "alpha_finish": alpha, "duration": duration}, renderer=renderer)
        storyboard.push_state('fade_screen', state)
        return Wait(duration)

    return create_event
