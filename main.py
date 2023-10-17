import os
import sys

import pygame
from map_builder import MapBuilder

PATH = os.path.abspath('.') + '/assets/'

if __name__ == '__main__':
    if __name__ == '__main__':
        pygame.init()
        pygame.display.set_caption("jRPG Game")
        screen_width = 320
        screen_height = 240
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()

        font = pygame.font.SysFont('Arial', 12, bold=True)

        cave_map = MapBuilder(PATH + 'cave/cave_map.tmx')

        cave_map_group = pygame.sprite.Group()
        debug_group = pygame.sprite.Group()

        cave_map.build_map(cave_map_group, debug_group)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Game Render
            cave_map_group.draw(screen)
            debug_group.draw(screen)

            # get tile position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            tile_x, tile_y = cave_map.point_to_tile(mouse_x, mouse_y)
            mouse_location = f"{tile_x}, {tile_y}"
            img = font.render(
                mouse_location, True, pygame.Color('black'), pygame.Color('white')
            )
            screen.blit(img, (mouse_x+2, mouse_y+20))

            pygame.display.flip()
            clock.tick(60)
