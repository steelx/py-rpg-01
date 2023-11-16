from typing import Protocol, runtime_checkable


@runtime_checkable
class Event(Protocol):

    def update(self, dt):
        ...

    def is_blocking(self) -> bool:
        ...

    def is_finished(self) -> bool:
        ...
