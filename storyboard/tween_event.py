"""
TweenEvent are pretty versatile (implements Event protocol), so instead of a FadeEvent we’ll create a TweenEvent that can
do the job of the FadeEvent and many more! The TweenEvent takes three parameters:
• tween - the Tween object.
• target - the target object the tween’s value is applied to.
• ApplyFunc - a function that controls how the tween value it applied to the target.

example: we can use the TweenEvent to fade in and out the screen, but we can also use to many more!
"""
from typing import Callable, Any

from tweener import Tween


class TweenEvent:
    def __init__(self, tween: Tween, target: Any, apply_func: Callable):
        self.tween = tween
        self.target = target
        self.apply_func = apply_func

    def is_blocking(self) -> bool:
        return True

    def is_finished(self) -> bool:
        return self.tween.animating is False

    def update(self, dt: float):
        self.tween.update()
        self.apply_func(self.target, self.tween.value)

    def __repr__(self) -> str:
        return f"TweenEvent(tween={self.tween}, apply_func={self.apply_func})"
