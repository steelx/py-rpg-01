from typing import Callable

import pygame

from storyboard import Storyboard, Event, Wait
from storyboard.states import FadeState


def fade_screen(id_: str, alpha_end: int, duration: float, renderer: pygame.Surface, alpha_start: int = 255) -> Callable[[Storyboard], Event]:
    def create_event(storyboard: Storyboard) -> Event:
        state = FadeState(
            params={"alpha_start": alpha_start, "alpha_end": alpha_end, "duration": duration},
            renderer=renderer)
        storyboard.push_state(id_, state)
        return Wait(duration, id_)

    return create_event
