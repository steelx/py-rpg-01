from typing import TypedDict, Optional, Callable, Union, Any

import pygame

# Define a Callable type for the ApplyFunc that takes a target and a value (assumed to be an integer)
ApplyFuncType = Callable[[Any, int], None]

# Define a Callable type for the Render function that takes several parameters
RenderFuncType = Callable[[str, pygame.Surface], None]


# Define the type for individual caption styles
class CaptionStyle(TypedDict, total=False):
    font: Optional[Union[str, pygame.font.Font]]  # Can be a string or a preloaded pygame Font object
    scale: Optional[float]
    alignX: Optional[str]
    alignY: Optional[str]
    x: Optional[int]
    y: Optional[int]
    color: Optional[pygame.Color]
    width: Optional[int]
    Render: Optional[RenderFuncType]
    ApplyFunc: Optional[ApplyFuncType]
    duration: Optional[float]


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
        self.style["Render"](self.style, self.text, display)

    def update(self, dt: float) -> None:
        pass

    def process_event(self, event: pygame.event.Event) -> None:
        pass
