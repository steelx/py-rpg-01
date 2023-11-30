from typing import Tuple

import pygame


# Make sure to initialize Pygame and your font before this
# pygame.init()
# custom_font = pygame.font.Font('path_to_your_font.ttf', font_size)

class DialogueBox:
    should_exit: bool = False

    def __init__(self, pos: Tuple[float, float], font: pygame.font.Font, text: str,
                 background_color=(0, 0, 0), text_color=(255, 255, 255), border_color=(255, 255, 255), border_width=3):
        # calculate the size of the box based on the font
        text_surface = font.render(text, True, text_color)
        size = (text_surface.get_width() + 20, text_surface.get_height() + 20)
        self.rect = pygame.Rect(*pos, *size)  # (x, y, width, height)
        self.font = font
        self.text = text
        self.background_color = background_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.surface = pygame.Surface(self.rect.size)
        self.text_surface = None
        self._build_textbox()

    def _build_textbox(self):
        # Clear the surface
        self.surface.fill(self.border_color)
        # Draw the background rectangle
        pygame.draw.rect(
            self.surface,
            self.background_color,
            (self.border_width, self.border_width, self.rect.width - self.border_width * 2,
             self.rect.height - self.border_width * 2)
        )
        # Render the text
        self.text_surface = self.font.render(self.text, True, self.text_color)
        # Blit the text to the surface
        text_rect = self.text_surface.get_rect(center=(self.rect.width / 2, self.rect.height / 2))
        self.surface.blit(self.text_surface, text_rect)

    def update_text(self, new_text):
        self.text = new_text
        self._build_textbox()

    def update(self, dt: float):
        pass

    def render(self, display: pygame.Surface):
        # Blit the dialogue box surface to the screen
        display.blit(self.surface, self.rect.topleft)

    def enter(self):
        pass

    def exit(self):
        pass

    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.should_exit = True
