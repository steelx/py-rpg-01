from typing import Tuple, Callable, List

import pygame
import pygame_gui
from pygame_gui.elements import UITextBox
from .chunk_message import chunk_message

from globals import ASSETS_PATH


class Textbox(pygame_gui.elements.UIPanel):
    def __init__(self, text: str, pos: Tuple[int, int], size: Tuple[int, int], chars_per_line: int,
                 lines_per_chunk: int, manager: pygame_gui.UIManager):
        super().__init__(
            relative_rect=pygame.Rect(pos, size),
            starting_height=1,
            manager=manager
        )
        self.elements = []
        self.manager = manager
        self.message_chunks = []
        self.current_chunk = 0
        self.arrow_indicator = None
        # Texbox scale size down a bit
        # size = (size[0]*0.8, size[1]*0.8)
        # pos = (pos[0] + size[0]*0.1, pos[1] + size[1]*0.1)
        self._create_textbox(text, pos, size, chars_per_line, lines_per_chunk)

    def _create_textbox(self, message: str, pos: Tuple[int, int], size: Tuple[int, int], chars_per_line: int,
                        lines_per_chunk: int, arrow_size=15) -> UITextBox:
        self.message_chunks = chunk_message(message, chars_per_line, lines_per_chunk)
        self.text_box = UITextBox(
            html_text=self.message_chunks[self.current_chunk],
            relative_rect=pygame.Rect(pos, size),
            manager=self.manager,
            container=self,
            object_id='@text_message',
            wrap_to_height=False
        )
        self.elements.append(self.text_box)

        if len(self.message_chunks) > 1:
            # If there are multiple chunks, add a down arrow indicator
            arrow_size = 15
            pos = (pos[0] + size[0] * 0.9, pos[1] + size[1] * 0.9)
            arrow_pos = (pos[0] - arrow_size, pos[1] - arrow_size)
            self.arrow_indicator = pygame_gui.elements.UIImage(
                pygame.Rect(arrow_pos, (arrow_size, arrow_size)),
                pygame.image.load(ASSETS_PATH + "ui/continue_caret.png").convert_alpha(),
                manager=self.manager,
                container=self
            )
            self.elements.append(self.arrow_indicator)

    def show_next_chunk(self, end_callback: Callable = None):
        """Show the next chunk of the message."""
        if self.current_chunk < len(self.message_chunks) - 1:
            self.current_chunk += 1
            self.text_box.html_text = self.message_chunks[self.current_chunk]
            self.text_box.rebuild()
            if self.current_chunk == len(self.message_chunks) - 1:
                self.arrow_indicator.kill()  # Remove the arrow when on the last chunk
        else:
            if end_callback:
                end_callback()
            else:
                self.kill()

    def update(self, dt: float):
        pass

    def render(self):
        pass

    def enter(self):
        self.visible = True
        for element in self.elements:
            element.visible = True

    def exit(self):
        self.visible = False
        for element in self.elements:
            element.visible = False

    def process_event(self, event: pygame.event.Event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.show_next_chunk()
