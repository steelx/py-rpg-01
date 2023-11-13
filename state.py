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
