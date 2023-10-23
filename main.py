import os
import sys
from typing import Dict, Any

import pygame

from actions import teleport
from entity import Entity, CharacterDefinition
from globals import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game import Game
from move_state import MoveState
from statemachine import StateMachine
from trigger import Trigger, ActionDef
from wait_state import WaitState

PATH = os.path.abspath('.') + '/assets/'

if __name__ == '__main__':
    if __name__ == '__main__':
        pygame.init()
        pygame.display.set_caption("jRPG Game")
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        cave_map = Game(PATH + 'small_room.tmx')
        cave_map.build_map()

        hero_controller = StateMachine({
            "wait": lambda: WaitState(hero, cave_map),
            "move": lambda: MoveState(hero, cave_map)
        })
        hero_def = CharacterDefinition(
            tile_x=9,
            tile_y=5,
            start_frame=8,
            height=24,
            width=16,
            texture_path=PATH + 'walk_cycle.png'
        )
        hero: Dict[str, Any] = {
            "anim": {
                "up": (0, 1, 2, 3),
                "right": (4, 5, 6, 7),
                "down": (8, 9, 10, 11),
                "left": (12, 13, 14, 15)
            },
            "entity": Entity.create(hero_def, cave_map),
            "controller": hero_controller
        }

        hero["controller"].change("wait")

        cave_map.follow = hero["entity"]

        teleport_from_top_door = teleport(cave_map, 10, 12)
        trigger_up_door = Trigger(ActionDef(
            on_enter=teleport_from_top_door
        ))

        cave_map.triggers = {
            '11,3': trigger_up_door
        }

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        up_door_teleport(None, hero["entity"])

            # Game Render
            screen.fill((0, 0, 0))
            cave_map.render()
            cave_map.update()
            hero["controller"].update()

            pygame.display.update()
            clock.tick(FPS)
