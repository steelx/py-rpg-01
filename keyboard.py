import sys

import pygame


class TileMovementHandler:
    """
    Takes user input and handles 1 key press with defined cooldown
    """
    def __init__(self, cooldown=500):
        self.cooldown = cooldown
        self.key_states = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False}
        self.movement_keys = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1)
        }
        self.movement = (0, 0)
        self.key_cooldowns = {key: 0 for key in self.movement_keys}

    def handle_input(self, movement_handler=lambda dx, dy: None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        for key in self.key_states:
            if keys[key] and self.key_states[key]:
                self.movement = self.movement_keys[key]
                dx, dy = self.movement
                movement_handler(dx, dy)
                self.key_states[key] = False
                self.key_cooldowns[key] = pygame.time.get_ticks()
            elif not self.key_states[key]:
                self.cooldown_key(key)

    def cooldown_key(self, key: int):
        current_time = pygame.time.get_ticks()
        if current_time - self.cooldown >= self.key_cooldowns[key]:
            self.key_states[key] = True

