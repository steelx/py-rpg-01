"""
# Usage Example:
screen = pygame.display.set_mode((800, 600))
caption_style = CaptionStyles['title']
caption_style.x = screen.get_width() // 2  # Center X
caption_style.y = 100  # Some Y position
caption_style.Render(caption_style, screen, "Your Game Title")
"""
import pygame

from storyboard.states import CaptionStylesType, CaptionStyle


# Renderer function adapted for Pygame
def default_renderer(style: CaptionStyle, text: str, screen: pygame.Surface):
    font = style.font if isinstance(style.font, pygame.font.Font) else pygame.font.SysFont(style.font, style.scale * 10)
    text_surface = font.render(text, True, style.color)
    text_rect = text_surface.get_rect()

    if style.alignX == 'center':
        text_rect.centerx = style.x if style.x else screen.get_rect().centerx
    if style.alignY == 'center':
        text_rect.centery = style.y if style.y else screen.get_rect().centery

    screen.blit(text_surface, text_rect)


def fade_apply(target: CaptionStyle, value: int):
    target.color.a = value


# Define caption styles
CaptionStyles: CaptionStylesType = {
    "default": CaptionStyle(
        font='Arial',
        scale=1,
        alignX='center',
        alignY='center',
        x=0,
        y=0,
        color=pygame.Color(255, 255, 255, 255),
        width=-1,
        Render=default_renderer,
        ApplyFunc=lambda target, value: None,
        duration=1
    ),
    "title": CaptionStyle(
        font='Arial',
        scale=3,
        y=100,
        color=pygame.Color(255, 255, 255, 255),
        Render=default_renderer,
        ApplyFunc=fade_apply,
        duration=1
    ),
    "subtitle": CaptionStyle(
        font='Consolas',
        scale=1,
        y=200,
        color=pygame.Color(255, 255, 99, 255),
        Render=default_renderer,
        ApplyFunc=fade_apply,
        duration=1
    )
}
