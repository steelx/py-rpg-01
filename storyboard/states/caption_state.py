from dataclasses import dataclass, field
from typing import TypedDict, Optional, Callable, Union, Any

import pygame

# Define a Callable type for the ApplyFunc that takes a target and a value (assumed to be an integer)
ApplyFuncType = Callable[[Any, int], None]

# Define a Callable type for the Render function that takes several parameters
RenderFuncType = Callable[[Any, str, pygame.Surface], None]


@dataclass
class CaptionStyle:
    font: Optional[Union[str, pygame.font.Font]] = 'Arial'
    scale: int = 1
    alignX: str = 'center'
    alignY: str = 'center'
    x: int = 0
    y: int = 0
    color: pygame.Color = field(default_factory=lambda: pygame.Color(255, 255, 255, 255))
    width: int = -1
    Render: Optional[RenderFuncType] = None
    ApplyFunc: Optional[ApplyFuncType] = None
    duration: float = 1.0


# Define the type for the entire CaptionStyles dictionary
CaptionStylesType = TypedDict('CaptionStylesType', {
    'default': CaptionStyle,
    'title': CaptionStyle,
    'subtitle': CaptionStyle,
})


class CaptionState:
    should_exit = False

    def __init__(self, style: CaptionStyle, text: str):
        self.style = style
        self.text = text

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def render(self, display: pygame.Surface) -> None:
        self.style.Render(self.style, self.text, display)

    def update(self, dt: float) -> None:
        pass

    def process_event(self, event: pygame.event.Event) -> None:
        pass
