import os
import pygame

from entity import Entity, CharacterDefinition
from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game
from keyboard import TileMovementHandler

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

        input_handler = TileMovementHandler()

        while True:
            # Input
            input_handler.handle_input(lambda dx, dy: hero.teleport(dx, dy))

            # Game Render
            cave_map.render()
            cave_map.update()

            # get tile position
            # mouse_x, mouse_y = pygame.mouse.get_pos()
            # tile_x, tile_y = cave_map.point_to_tile(mouse_x, mouse_y)
            # print(f"Tile {tile_x}, {tile_y}")

            pygame.display.update()
            clock.tick(60)
