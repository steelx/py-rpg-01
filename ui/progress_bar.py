from typing import Tuple

import pygame


class ProgressBar:
    def __init__(self, position: Tuple[int, int], bar_size: Tuple[int, int],
                 background_image: str, foreground_image: str, max_hp: int, surface: pygame.Surface):
        self.background = pygame.image.load(background_image).convert_alpha()
        self.foreground = pygame.image.load(foreground_image).convert_alpha()
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.surface = surface
        self.position = position
        self.bar_size = bar_size

    def update(self, current_hp: int, position: Tuple[int, int] = None):
        if position:
            self.position = position
        self.current_hp = current_hp

    def draw(self):
        # Draw the background
        background_surf = pygame.Surface(self.bar_size, pygame.SRCALPHA).convert_alpha()
        background_surf.blit(self.background, (0, 0))
        self.surface.blit(background_surf, self.position)

        # Calculate the width of the foreground based on current HP
        foreground_width = (self.current_hp / self.max_hp) * self.bar_size[0]
        # Create a new surface for the foreground with alpha transparency
        foreground_surf = pygame.Surface(self.bar_size, pygame.SRCALPHA).convert_alpha()
        foreground_surf.blit(self.foreground, (0, 0), (0, 0, foreground_width, self.bar_size[1]))

        # Draw the foreground surface on top of the background
        self.surface.blit(foreground_surf, self.position)
