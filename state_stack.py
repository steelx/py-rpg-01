from typing import Protocol, List, Optional

import pygame
import pygame_gui


class StackInterface(Protocol):
    should_exit: bool

    def enter(self, **kwargs) -> None:
        ...

    def exit(self) -> None:
        ...

    def render(self) -> None:
        ...

    def update(self, dt: float) -> None:
        ...

    def process_event(self, event):
        ...


class StateStack:
    """
    In StateStack each state is a UI element that is rendered on top of each other.
    But only the top state is updated and process_event.
    """
    def __init__(self, manager: pygame_gui.UIManager):
        self.states: List[StackInterface] = []
        self.manager = manager

    def push(self, state: StackInterface):
        if self.states:
            self.states[-1].exit()
        self.states.append(state)
        state.enter()

    def pop(self) -> Optional[StackInterface]:
        if self.states:
            top_state = self.states.pop()
            top_state.exit()
            if self.states:
                self.states[-1].enter()
            return top_state
        return None

    def top(self) -> Optional[StackInterface]:
        if self.states:
            return self.states[-1]
        return None

    def update(self, dt: float):
        self.manager.update(dt)
        if self.states:
            self.states[-1].update(dt)
            if self.states[-1].should_exit:
                self.pop()

    def draw(self, screen: pygame.Surface):
        self.manager.draw_ui(screen)
        for state in self.states:
            state.render()

    def process_event(self, event: pygame.event.Event):
        if self.states:
            self.states[-1].process_event(event)

    def is_empty(self) -> bool:
        return len(self.states) == 0

    def __str__(self):
        return '\n'.join(str(state) for state in self.states)
