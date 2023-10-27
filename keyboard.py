import sys
import time

import pygame


class TileMovementHandler:
    """
    Takes user input and handles 1 key press with defined cooldown
    """

    def __init__(self, cooldown=0.08):
        self.cooldown = cooldown
        self.movement_keys = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1)
        }
        self.key_pressed = {key: False for key in self.movement_keys}
        self.key_last_press_time: dict[int, float] = {
            key: 0 for key in self.movement_keys}

    def reset_key_pressed(self):
        for k in self.key_pressed:
            self.key_pressed[k] = False

    def handle_input(self, movement_handler=lambda dx, dy: None):
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in self.movement_keys:
                    self.key_last_press_time[event.key] = current_time
                    self.key_pressed[event.key] = True

            if event.type == pygame.KEYUP:
                if event.key in self.movement_keys:
                    self.key_pressed[event.key] = False

        # check if key is pressed and if cooldown is over
        for key in self.key_pressed:
            if self.key_pressed[key]:
                if self.cooldown_over(key):
                    self.key_last_press_time[key] = time.time()
                    dx, dy = self.movement_keys[key]
                    movement_handler(dx, dy)

    def cooldown_over(self, key):
        return (time.time() - self.key_last_press_time[key]) >= self.cooldown
