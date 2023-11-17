from typing import Callable

from storyboard import Storyboard, Event, Wait


def remove_state(id_: str) -> Callable[[Storyboard], Event]:
    def create_event(storyboard: Storyboard) -> Event:
        storyboard.remove_state(id_)
        return Wait(0)

    return create_event


def no_blocking(func: Callable[[Storyboard], Event]):
    def create_event(storyboard: Storyboard) -> Event:
        e = func(storyboard)
        e.is_blocking = lambda: False
        return e

    return create_event
