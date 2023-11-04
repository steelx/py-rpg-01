# dialogue_panel.py
from typing import Tuple, List
import pygame
import pygame_gui
from globals import WINDOW_SIZE, ASSETS_PATH
from ui import Panel

AVATAR_WIDTH_RATIO = 0.15


def chunk_message(message: str, chars_per_line: int = 68, lines_per_chunk: int = 3) -> List[str]:
    """Break the message into chunks based on characters per line and lines per chunk."""
    def split_line(s: str, chars: int) -> List[str]:
        """Helper function to split a string respecting word boundaries."""
        lines = []
        while len(s) > chars:
            idx = s.rfind(' ', 0, chars)
            if idx == -1:  # If no spaces found, just split the word.
                idx = chars
            line = s[:idx].strip()
            if line:  # Only add non-empty lines
                lines.append(line)
            s = s[idx:].strip()
        if s:
            lines.append(s)
        return lines

    # Remove all newline characters and create a continuous string
    message = message.replace('\n', ' ').replace('\r', '').strip()

    # Split the message respecting word boundaries
    lines = split_line(message, chars_per_line)

    # Group lines into chunks
    return ["\n".join(lines[i:i + lines_per_chunk]) for i in range(0, len(lines), lines_per_chunk)]


class DialoguePanel(Panel):
    def __init__(self, manager: pygame_gui.UIManager, window_size: Tuple[int, int] = WINDOW_SIZE, **kwargs):
        bottom_panel_height = int(0.30 * window_size[1])
        super().__init__(
            0, window_size[1] - bottom_panel_height, window_size[0], bottom_panel_height, manager, **kwargs
        )
        self.message_chunks = []
        self.current_chunk = 0
        self.text_box = None
        self.arrow_indicator = None

    def setup_dialogue(self, hero_image: str, hero_name: str, message: str):
        self.message_chunks = chunk_message(message, lines_per_chunk=3)
        self.add_image(hero_image)
        self.add_title_and_message(hero_name, self.message_chunks[self.current_chunk])

    def show_next_chunk(self):
        """Show the next chunk of the message."""
        if self.current_chunk < len(self.message_chunks) - 1:
            self.current_chunk += 1
            self.text_box.html_text = self.message_chunks[self.current_chunk]
            self.text_box.rebuild()
            if self.current_chunk == len(self.message_chunks) - 1:
                self.arrow_indicator.kill()  # Remove the arrow when on the last chunk
        else:
            self.kill()

    def add_image(self, image_path: str, pos: Tuple[int, int] = (5, 5)):
        avatar_size = (self.rect.width * AVATAR_WIDTH_RATIO, self.rect.height * 0.75)
        image_surface = pygame.image.load(image_path).convert_alpha()

        # Preserving aspect ratio while scaling
        aspect_ratio = image_surface.get_width() / image_surface.get_height()
        new_width = avatar_size[0]
        new_height = int(new_width / aspect_ratio)

        if new_height > avatar_size[1]:
            new_height = avatar_size[1]
            new_width = int(new_height * aspect_ratio)

        image_surface = pygame.transform.scale(image_surface, (new_width, new_height))

        avatar = pygame_gui.elements.UIImage(
            pygame.Rect(pos, (new_width, new_height)),
            image_surface,
            manager=self.ui_manager,
            container=self
        )
        return avatar

    def add_title_and_message(self, title: str, message: str, pos: Tuple[int, int] = (125, 5)):
        line_height = 25
        size = (self.rect.width * (1 - AVATAR_WIDTH_RATIO), line_height)
        size = (size[0] - 40, size[1])
        # title_label
        pygame_gui.elements.UITextBox(
            title,
            pygame.Rect(pos, size),
            manager=self.ui_manager,
            container=self,
            object_id='@text_title'
        )
        pos = (pos[0], pos[1] + line_height)
        size = (size[0], self.rect.height * 0.50)
        self.text_box = pygame_gui.elements.UITextBox(
            message,
            pygame.Rect(pos, size),
            manager=self.ui_manager,
            container=self,
            object_id='@text_message',
            wrap_to_height=False,
        )

        if len(self.message_chunks) > 1:
            # If there are multiple chunks, add a down arrow indicator
            arrow_size = 15
            arrow_pos = (pos[0] + size[0] - arrow_size, pos[1] + size[1] - arrow_size)
            self.arrow_indicator = pygame_gui.elements.UIImage(
                pygame.Rect(arrow_pos, (arrow_size, arrow_size)),
                pygame.image.load(ASSETS_PATH+"ui/continue_caret.png").convert_alpha(),
                manager=self.ui_manager,
                container=self
            )
