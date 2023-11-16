"""
A simple state machine implementation.
example: A state machine for a game menu, characters, etc.
A Main Menu can be in State Stack, while its submenus are in State Machine.
in State machine current state is always active, while in State Stack, only the top state is active.
in state machine, you can change state, while in state stack, you can push and pop state.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class State(Protocol):
    def enter(self, **kwargs) -> None:
        ...

    def exit(self) -> None:
        ...

    def render(self, **kwargs) -> None:
        ...

    def update(self, dt) -> None:
        ...

    def process_event(self, event) -> None:
        ...


class StateMachine:
    states: dict[str, State]
    current: State | None

    def __init__(self, states: dict[str, State]):
        self.states = states
        self.current = None

    def add(self, state_name, state: State):
        self.states[state_name] = state

    def change(self, state_name, **kwargs):
        if self.current is not None:
            self.current.exit()

        self.current = self.states[state_name]
        self.current.enter(**kwargs)

    def update(self, dt):
        self.current.update(dt)

    def render(self, **kwargs):
        self.current.render(**kwargs)

    def process_event(self, event):
        self.current.process_event(event)
