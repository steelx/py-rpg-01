"""
TweenEvent are pretty versatile (implements Event protocol), so instead of a FadeEvent we’ll create a TweenEvent that can
do the job of the FadeEvent and many more! The TweenEvent takes three parameters:
• tween - the Tween object.
• target - the target object the tween’s value is applied to.
• ApplyFunc - a function that controls how the tween value it applied to the target.

example: we can use the TweenEvent to fade in and out the screen, but we can also use to many more!
"""
from typing import Callable

from utils.tween import TweenTo


class TweenEvent:
    def __init__(self, tween: TweenTo, apply_func: Callable):
        self.tween = tween
        self.apply_func = apply_func

    def is_blocking(self) -> bool:
        return True

    def is_finished(self) -> bool:
        return self.tween.is_finished()

    def update(self, dt: float):
        self.tween.update(dt)
        self.apply_func()

    def __repr__(self) -> str:
        return f"TweenEvent(tween={self.tween}, apply_func={self.apply_func})"
