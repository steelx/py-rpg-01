from typing import Tuple

import pygame
import pygame_gui
from pygame_gui.core import IContainerLikeInterface


def create_textbox(html_text: str, pos: Tuple[float, float], size: Tuple[float, float], manager: pygame_gui.UIManager,
                   container: IContainerLikeInterface = None):
    return pygame_gui.elements.UITextBox(
        html_text=html_text,
        relative_rect=pygame.Rect(*pos, *size),
        manager=manager,
        starting_height=10,
        container=container,
        object_id='@text_message',
        wrap_to_height=True
    )


def create_title(html_text: str, pos: Tuple[float, float], size: Tuple[float, float], manager: pygame_gui.UIManager,
                 container: IContainerLikeInterface = None):
    return pygame_gui.elements.UITextBox(
        html_text=html_text,
        relative_rect=pygame.Rect(*pos, *size),
        manager=manager,
        starting_height=10,
        container=container,
        object_id='@text_title_big',
        wrap_to_height=True
    )