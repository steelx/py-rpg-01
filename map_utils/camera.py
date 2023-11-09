from typing import Tuple

import pygame


class Camera:
    def __init__(self, game, width_pixel, height_pixel):
        self.game = game
        self.x = 0
        self.y = 0
        self.width_pixel = width_pixel
        self.height_pixel = height_pixel
        self.follow = None

    def set_follow(self, entity: pygame.sprite.Sprite):
        self.follow = entity

    def get_position(self):
        return self.x, self.y

    def follow_entity(self):
        target_x, target_y = self.follow.rect.center
        self.go_to(target_x, target_y)

    def go_to(self, x: int, y: int, lerp_factor: float = 0.1):
        display_size = self.game.display_surface.get_size()

        # Calculate the target camera position centered on the target coordinates
        target_x = x - display_size[0] // 2
        target_y = y - display_size[1] // 2

        # Apply lerp to smoothly transition the camera to the target position
        self.x += (target_x - self.x) * lerp_factor
        self.y += (target_y - self.y) * lerp_factor
        # self._clamp_camera(display_size)

    def _clamp_camera(self, display_size: Tuple[float, float]):
        # Ensure the camera doesn't move beyond the map edges
        self.x = max(self.x, 0)
        self.y = max(self.y, 0)
        self.x = min(self.x, self.width_pixel + display_size[0])
        self.y = min(self.y, self.height_pixel + display_size[1])
