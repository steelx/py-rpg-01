from typing import Callable

import pygame.font
from tweener import Tween

from storyboard import Storyboard, Event, TweenEvent
from storyboard.caption_styles import CaptionStyles
from storyboard.states import CaptionState


def caption(id_: str, style_name: str, text: str, font: pygame.font.Font = None) -> Callable[[Storyboard], Event]:

    def create_event(storyboard: Storyboard) -> Event:
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
