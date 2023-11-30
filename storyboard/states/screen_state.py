"""
ScreenState implements the stack state protocol, it is a state that can be pushed to the stack.
"""
import pygame


class ScreenState:
    should_exit: bool = False

    def __init__(self, color=(0, 0, 0, 1)):
        self.color = pygame.Color(color)

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def render(self, display: pygame.Surface) -> None:
        overlay = pygame.Surface(display.get_size(), pygame.SRCALPHA)
        overlay.fill(self.color)
        display.blit(overlay, (0, 0))

    def update(self, dt: float) -> None:
        pass

    def process_event(self, event: pygame.event.Event) -> None:
        pass
