from typing import List, Optional, Callable, Union, Dict, Any

import pygame

from state_stack import StateStack, StackInterface
from storyboard import Event

EventCreator = Callable[[Any], Event]


class Storyboard:
    should_exit: bool = False

    def __init__(self, stack: StateStack, events: List[Union[Event, EventCreator]],
                 display: pygame.Surface,
                 font: pygame.font.Font):
        self.stack = stack
        self.events = events
        self.display = display
        self.font = font
        self.sub_stack = StateStack()
        self._stacks: Dict[str, StackInterface] = {}
        from storyboard import SoundEvent
        self._playing_sounds: Dict[str, SoundEvent] = {}

    def push_state(self, id: str, state: StackInterface):
        self._stacks[id] = state  # push a State on the stack but keep a reference here
        self.sub_stack.push(state)

    def remove_state(self, id_: str):
        state = self._stacks.pop(id_, None)  # Remove from the dictionary
        for v in self.sub_stack.states:
            if v == state:
                self.sub_stack.states.remove(v)
                break

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        # stop all sounds
        for v in self._playing_sounds.values():
            v.stop()

    def render(self, display) -> None:
        self.sub_stack.render(display)
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
        for idx, v in enumerate(self.events):
            # Check if event is a function and call it to get the Event instance
            if callable(v):
                self.events[idx] = v(self)
                v = self.events[idx]

            v.update(dt)
            if v.is_finished():
                delete_index = idx
                break
            if v.is_blocking():
                break

        if delete_index is not None:
            self.events.pop(delete_index)

    def process_event(self, event: pygame.event.Event):
        pass

    def cleanup(self):
        pass

    def add_sound(self, sound_id, event):
        self._playing_sounds[sound_id] = event

    def stop_sound(self, sound_id):
        self._playing_sounds[sound_id].stop()
        self._playing_sounds.pop(sound_id)
