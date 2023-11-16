"""
WaitEvent implements Event Protocol, checks if the event is a wait event.
"""


class Wait:
    def __init__(self, seconds: float, id_: str = None):
        self.id_ = id_
        self.seconds = seconds * 1000  # convert to milliseconds

    def update(self, dt):
        self.seconds -= dt

    def is_blocking(self) -> bool:
        return True

    def is_finished(self) -> bool:
        return self.seconds <= 0
