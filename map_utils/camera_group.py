import pygame


class CameraGroup(pygame.sprite.Group):
    def __init__(self, display: pygame.Surface = None):
        super().__init__()
        self.display_surface = display if display is not None else pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, cam_x: float, cam_y: float, sort=False):
        self.offset.x = cam_x
        self.offset.y = cam_y

        # no sorted for now since it's causing a bug with the player in tweening
        # Sort sprites by their bottom position
        sorted_sprites = sorted(self.sprites(), key=lambda s: s.rect.bottomright[1])

        for sprite in sorted_sprites if sort else self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)