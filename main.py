# This is a sample Python script.
import math
import os
import sys

import pygame

PATH = os.path.abspath('.') + '/assets/'

gMap = [
    0, 0, 0, 0, 4, 5, 6, 0,
    0, 0, 0, 0, 4, 5, 6, 0,
    0, 0, 0, 0, 4, 5, 6, 0,
    2, 2, 2, 2, 10, 5, 6, 0,
    8, 8, 8, 8, 8, 8, 9, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 2,
]
gMapWidth = 8
gMapHeight = 7


def get_tile(tile_map: list[int], row_size: int, x: int, y: int):
    return tile_map[x + y * row_size]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if __name__ == '__main__':

        pygame.init()
        pygame.display.set_caption("jRPG Game")
        screen_width = 800
        screen_height = 600
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()
        g_center = screen.get_rect().center

        grass_tile = pygame.image.load(PATH + 'grass_tile.png').convert_alpha()
        # grass_tile = pygame.transform.scale(grass_tile, (32, 32))
        g_tiles_per_row = math.ceil(pygame.display.get_surface().get_width() / grass_tile.get_width())
        g_tiles_per_col = math.ceil(pygame.display.get_surface().get_height() / grass_tile.get_height())

        print(f"Tiles per row: {g_tiles_per_row}")
        print(f"Tiles per col: {g_tiles_per_col}")

        gTextures = pygame.sprite.Group()
        for i in range(11):
            image = pygame.image.load(PATH + f"grass_tiles/tiles_{i:02d}.png").convert_alpha()
            sprite = pygame.sprite.Sprite()
            sprite.image = image
            sprite.rect = image.get_rect()
            gTextures.add(sprite)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Game Update
            for x in range(g_tiles_per_row):
                for y in range(g_tiles_per_col):
                    (pygame.display.get_surface()
                     .blit(grass_tile,(x * grass_tile.get_width(), y * grass_tile.get_height())))

            for j in range(gMapHeight):
                for i in range(gMapWidth):
                    tile = get_tile(gMap, gMapWidth, i, j)
                    sprite = gTextures.sprites()[tile]
                    rect = sprite.rect
                    w = rect.width
                    h = rect.height
                    pygame.display.get_surface().blit(sprite.image, (i * w, j * h))

            pygame.display.flip()
            clock.tick(60)
