from typing import Dict, Any

import pygame

from state_stack import StateStack
from utils.tween import TweenTo


class FadeState:
    should_exit = False

    def __init__(self, params: Dict[str, Any], renderer: pygame.Surface, stack: StateStack = None):
        self.stack = stack
        self.duration = params.get("duration", 1.0)
        self.alpha_start = params.get("alpha_start", 255)
        self.alpha_end = params.get("alpha_end", 0)
        self.color = pygame.Color(params.get("color", (0, 0, 0)))
        self.color.a = self.alpha_start
        self.overlay = pygame.Surface(renderer.get_size(), pygame.SRCALPHA)
        self.overlay.fill(self.color)
        self.tween = TweenTo(self.color, key="a", finish=self.alpha_end, duration=self.duration)

    def enter(self, **kwargs) -> None:
        pass

    def exit(self) -> None:
        pass

    def update(self, dt: float) -> None:
        self.tween.update(dt)
        if self.tween.is_finished():
            self.should_exit = True

    def render(self, renderer: pygame.Surface) -> None:
        self.overlay.fill(self.color)
        renderer.blit(self.overlay, (0, 0))

    def process_event(self, event: pygame.event.Event):
        pass
