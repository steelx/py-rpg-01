import os
import pygame
import sys

from entity import Entity, CharacterDefinition
from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game

PATH = os.path.abspath('.') + '/assets/'

if __name__ == '__main__':
    if __name__ == '__main__':
        pygame.init()
        pygame.display.set_caption("jRPG Game")
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        cave_map = Game(PATH + 'small_room.tmx')

        cave_map.setup()
        cave_map.go_to_tile(6, 5)

        hero = Entity.create(CharacterDefinition(
            tile_x=10,
            tile_y=2,
            start_frame=8,
            height=24,
            width=16,
            texture_path=PATH + 'walk_cycle.png'
        ), cave_map)

        # simulate just pressed
        movement_keys = {pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0), pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1)}
        movement = (0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in movement_keys:
                        movement = movement_keys[event.key]

                if event.type == pygame.KEYUP:
                    if event.key in movement_keys:
                        movement = (0, 0)

            # Handle hero movement
            hero.tile_x += movement[0]
            hero.tile_y += movement[1]
            hero.teleport()

            # Game Render
            cave_map.render()
            cave_map.update()

            # get tile position
            # mouse_x, mouse_y = pygame.mouse.get_pos()
            # tile_x, tile_y = cave_map.point_to_tile(mouse_x, mouse_y)
            # print(f"Tile {tile_x}, {tile_y}")

            pygame.display.update()
            clock.tick(60)
