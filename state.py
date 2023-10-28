from typing import Protocol


class State(Protocol):
    def enter(self, **kwargs) -> None:
        ...

    def exit(self) -> None:
        ...

    def render(self, **kwargs) -> None:
        ...

    def update(self, **kwargs) -> None:
        ...
