from typing import Callable

from storyboard import Storyboard, Event, Wait
from storyboard.states import ScreenState


def black_screen(id_: str = 'black_screen', alpha: int = 100) -> Callable[[Storyboard], Event]:
    def create_event(storyboard: Storyboard) -> Event:
        state = ScreenState(color=(0, 0, 0, alpha))
        storyboard.push_state(id_, state)
        return Wait(0.5)

    return create_event
