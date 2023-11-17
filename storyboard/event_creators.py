from typing import Callable

import pygame
from tweener import Tween

from storyboard import Storyboard, Event, Wait, TweenEvent
from storyboard.states import FadeState, ScreenState, CaptionState


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


def fade_screen(id_: str, alpha_end: int, duration: float, renderer: pygame.Surface, alpha_start: int = 255) -> Callable[[Storyboard], Event]:
    def create_event(storyboard: Storyboard) -> Event:
        state = FadeState(
            params={"alpha_start": alpha_start, "alpha_end": alpha_end, "duration": duration},
            renderer=renderer)
        storyboard.push_state(id_, state)
        return Wait(duration, id_)

    return create_event


def black_screen(id_: str = 'black_screen') -> Callable[[Storyboard], Event]:
    def create_event(storyboard: Storyboard) -> Event:
        state = ScreenState(color=(0, 0, 0, 255))
        storyboard.push_state(id_, state)
        return Wait(0, id_)

    return create_event


def caption(id_: str, style_name: str, text: str, font: pygame.font.Font = None) -> Callable[[Storyboard], Event]:
    def create_event(storyboard: Storyboard) -> Event:
        from storyboard.caption_styles import CaptionStyles
        # noinspection PyTypedDict
        _style = CaptionStyles.get(style_name, CaptionStyles['default'])
        if font is not None:
            _style.font = font
        state = CaptionState(_style, text)
        storyboard.push_state(id_, state)
        tween = Tween(0, 1, _style.duration)
        return TweenEvent(
            tween=tween,
            target=state.style,
            apply_func=_style.ApplyFunc,
        )

    return create_event
