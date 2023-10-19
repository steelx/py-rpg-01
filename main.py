import os
import pygame
import sys
from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game

PATH = os.path.abspath('.') + '/assets/'

if __name__ == '__main__':
    if __name__ == '__main__':
        pygame.init()
        pygame.display.set_caption("jRPG Game")
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        cave_map = Game(PATH + 'cave/cave_map.tmx')

        cave_map.setup()
        cave_map.go_to_tile(15, 18)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Game Render
            cave_map.render()
            cave_map.update()

            # get tile position
            # mouse_x, mouse_y = pygame.mouse.get_pos()
            # tile_x, tile_y = cave_map.point_to_tile(mouse_x, mouse_y)
            # mouse_location = f"{tile_x}, {tile_y}"
            # print(mouse_location)

            pygame.display.update()
            clock.tick(60)
