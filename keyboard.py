import sys

import pygame


class TileMovementHandler:
    """
    Takes user input and handles 1 key press with defined cooldown
    """
    def __init__(self):
        self.movement_keys = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1)
        }
        self.movement = (0, 0)
        self.key_cooldown = {key: 0 for key in self.movement_keys}

    def handle_input(self, movement_handler=lambda dx, dy: None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP:
                if event.key in self.movement_keys:
                    self.movement = self.movement_keys[event.key]
                    self.key_cooldown[event.key] = 4
                    dx, dy = self.movement
                    movement_handler(dx, dy)
