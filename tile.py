from pygame import Surface
from pygame.sprite import Sprite, Group


class Tile(Sprite):
    def __init__(self, pos: tuple[int, int], image: Surface, group: Group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
