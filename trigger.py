from dataclasses import dataclass, field
from typing import Optional, Callable


@dataclass
class ActionDef:
    on_enter: Optional[Callable] = field(default=None, repr=False)
    on_exit: Optional[Callable] = field(default=None, repr=False)
    on_use: Optional[Callable] = field(default=None, repr=False)


class Trigger:
    @staticmethod
    def empty_function(*args, **kwargs):
        """Default empty function."""
        pass

    def __init__(self, definition: ActionDef):
        self.onEnter = definition.on_enter or self.empty_function
        self.onExit = definition.on_exit or self.empty_function
        self.onUse = definition.on_use or self.empty_function
