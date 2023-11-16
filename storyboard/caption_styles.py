"""
# Usage Example:
screen = pygame.display.set_mode((800, 600))
caption_style = CaptionStyles['title']
caption_style['x'] = screen.get_width() // 2  # Center X
caption_style['y'] = 100  # Some Y position
caption_style['Render'](caption_style, screen, "Your Game Title")
"""
import pygame

from storyboard.states import CaptionStylesType, CaptionStyle


# Renderer function adapted for Pygame
def default_renderer(style_: CaptionStyle, text: str, screen: pygame.Surface):
    font = style_['font'] if isinstance(style_['font'], pygame.font.Font) else pygame.font.SysFont(style_['font'],
                                                                                                   style_['scale'] * 10)

    text_surface = font.render(text, True, style_['color'])
    text_rect = text_surface.get_rect()

    if style_['alignX'] == 'center':
        text_rect.centerx = style_['x'] if style_['x'] else screen.get_rect().centerx
    if style_['alignY'] == 'center':
        text_rect.centery = style_['y'] if style_['y'] else screen.get_rect().centery

    screen.blit(text_surface, text_rect)


def fade_apply(target: CaptionStyle, value: int):
    target['color'].a = value


# Define caption styles
CaptionStyles: CaptionStylesType = {
    "default": {
        'font': 'Arial',
        'scale': 1,
        'alignX': 'center',
        'alignY': 'center',
        'x': 0,
        'y': 0,
        'color': pygame.Color(255, 255, 255, 255),
        'width': -1,
        'Render': default_renderer,
        'ApplyFunc': lambda target, value: None,
        'duration': 1
    },
    "title": {
        'font': 'Arial',
        'scale': 3,
        'y': 75,
        'Render': default_renderer,
        'ApplyFunc': fade_apply,
        'duration': 3
    },
    "subtitle": {
        'scale': 1,
        'y': -5,
        'color': pygame.Color(102, 97, 99, 255),
        'Render': default_renderer,
        'ApplyFunc': fade_apply,
        'duration': 1
    }
}

# Set caption defaults
for name, style in CaptionStyles.items():
    if name != "default":
        for k, v in CaptionStyles["default"].items():
            style.setdefault(k, v)
