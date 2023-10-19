from pygame import Surface, SRCALPHA
from pygame.sprite import Sprite, Group


class Tile(Sprite):
    def __init__(self, pos: tuple[int, int], image: Surface, group: Group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


class Circle(Sprite):
    def __init__(self, pos: tuple[int, int], radius: int, color: str, group: Group):
        super().__init__(group)
        self.image = Surface((2 * radius, 2 * radius), SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)


class Rectangle(Sprite):
    def __init__(self, pos: tuple[int, int], width: int, height: int, color: str, group: Group):
        super().__init__(group)
        self.image = Surface((width, height), SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)


class Entity(Sprite):
    def __init__(self, pos: tuple[int, int], image: Surface, group: Group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        pass
