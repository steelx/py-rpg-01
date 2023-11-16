from typing import List, Optional, Callable, Union, Dict, Any

import pygame

from state_stack import StateStack, StackInterface, SubStateStack
from storyboard import Event

EventCreator = Callable[[Any], Event]


class Storyboard:
    should_exit: bool = False

    def __init__(self, stack: StateStack, events: List[Union[Event, EventCreator]], display: pygame.Surface,
                 font: pygame.font.Font):
        self.stack = stack
        self.events = events
        self.display = display
        self.font = font
        self.sub_stack = SubStateStack()
        self._stacks: Dict[str, StackInterface] = {}

    def push_state(self, id: str, state: StackInterface):
        self._stacks[id] = state  # push a State on the stack but keep a reference here
        self.sub_stack.push(state)

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def render(self) -> None:
        self.sub_stack.render(self.display)
        # debug info
        info = f"{self.events[-1].__class__.__name__} ({len(self.events)})" if len(self.events) > 0 else len(
            self.events)
        debug_text = f"Events Stack: {info}"
        text = self.font.render(debug_text, True, (255, 255, 255))
        self.display.blit(text, (0, 0))

    def update(self, dt: float) -> None:
        if len(self.events) == 0:
            self.should_exit = True
            return

        self.sub_stack.update(dt)

        delete_index: Optional[int, None] = None
        for k, v in enumerate(self.events):
            # Check if event is a function and call it to get the Event instance
            if callable(v):
                self.events[k] = v(self)
                v = self.events[k]

            v.update(dt)
            if v.is_finished():
                delete_index = k
                break
            if v.is_blocking():
                break

        if delete_index is not None:
            self.events.pop(delete_index)

    def process_event(self, event: pygame.event.Event):
        pass

    def cleanup(self):
        pass