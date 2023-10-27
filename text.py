import pygame.font


class Text:
    def __init__(self, text: str, x: float, y: float, font_name='Arial', font_size=24, color=(255, 255, 255)):
        """
        :param text: Text to be displayed.
        :param x: X-coordinate for the text position.
        :param y: Y-coordinate for the text position.
        :param font_name: Name of the font or path to .ttf file. None for pygame default.
        :param font_size: Size of the font.
        :param color: Color of the font as a tuple (R, G, B).
        """
        self.text = text
        self.pos = (x, y)
        self.font = pygame.font.SysFont(font_name, font_size)
        self.color = color
        self._rendered_text = None
        self._text_rect = None
        self.update_render()

    def update_render(self):
        """Renders the text and caches the result."""
        self._rendered_text = self.font.render(self.text, True, self.color)
        self._text_rect = self._rendered_text.get_rect()
        self._text_rect.topleft = self.pos

    def update_position(self, position: tuple[float, float]):
        print(position)
        self.pos = position

    def set_text(self, new_text):
        """Sets a new text and updates the rendered image."""
        self.text = new_text
        self.update_render()

    def draw(self, surface):
        """Draws the text on the given surface."""
        surface.blit(self._rendered_text, self._text_rect)
