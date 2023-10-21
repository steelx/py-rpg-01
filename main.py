import os
from typing import Dict, Any

import pygame

from entity import Entity, CharacterDefinition
from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game
from move_state import MoveState
from statemachine import StateMachine
from wait_state import WaitState

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

        hero_controller = StateMachine({
            "wait": lambda: WaitState(hero, cave_map),
            "walk": lambda: MoveState(hero, cave_map)
        })

        hero: Dict[str, Any] = {
            "entity": Entity.create(CharacterDefinition(
                tile_x=10,
                tile_y=2,
                start_frame=8,
                height=24,
                width=16,
                texture_path=PATH + 'walk_cycle.png'
            ), cave_map),
            "controller": hero_controller
        }

        hero["controller"].change("wait")

        while True:
            # Game Render
            cave_map.render()
            cave_map.update()
            hero["controller"].update()

            pygame.display.update()
            clock.tick(60)
