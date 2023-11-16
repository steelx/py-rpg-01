from typing import Callable

import pygame.font
from tweener import Tween

from storyboard import Storyboard, Event, TweenEvent
from storyboard.caption_styles import CaptionStyles
from storyboard.states import CaptionState


def caption(id_: str, style: str, text: str, font: pygame.font.Font = None) -> Callable[[Storyboard], Event]:

    def create_event(storyboard: Storyboard) -> Event:
        style_ = CaptionStyles.get(style, CaptionStyles['default'])
        if font is not None:
            style_['font'] = font
        state = CaptionState(style_, text)
        storyboard.push_state(id_, state)
        tween = Tween(0, 1, style_["duration"])
        return TweenEvent(
            tween=tween,
            target=state.style,
            apply_func=style_["ApplyFunc"]
        )

    return create_event
