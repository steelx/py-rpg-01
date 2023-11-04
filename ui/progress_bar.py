from typing import Tuple

import pygame
import pygame_gui
from pygame_gui import UIManager


class ProgressBar:
    progress_bar: pygame_gui.elements.UIProgressBar
    label: pygame_gui.elements.UILabel

    def __init__(self, rect: pygame.Rect, manager: UIManager,
                 start_progress: float, text='HP', text_rect_offset=(-5, -20), object_id='@progress_bar'):
        self.manager = manager

        # Create the progress bar
        self.progress_bar = pygame_gui.elements.UIProgressBar(
            relative_rect=rect, manager=manager, visible=True, object_id=object_id,
        )
        self.progress_bar.set_current_progress(start_progress)

        # Create the label for text
        text_rect = pygame.Rect((rect.x + text_rect_offset[0], rect.y + text_rect_offset[1]), (50, 25))
        self.label = pygame_gui.elements.UILabel(relative_rect=text_rect, text=text, manager=manager, object_id=object_id)

    def set_progress(self, value):
        self.progress_bar.set_current_progress(value)

    def update(self, time_delta):
        # Any additional updates can be handled here if necessary
        pass

    def draw(self):
        # In the case of pygame_gui, drawing is handled by the UIManager
        pass

    def update_position(self, pos: Tuple[float, float]):
        self.progress_bar.set_position((pos[0] - 20, pos[1] - 70))
        self.label.set_position((pos[0] - 25, pos[1] - 90))
