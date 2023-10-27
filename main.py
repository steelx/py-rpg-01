import os
import sys

import pygame

from actions import teleport, ACTIONS
from character import Character
from character_definitions import characters
from game import Game
from globals import FPS, WINDOW_SIZE, DISPLAY_SIZE
from map_definitions import MapDefinition, ActionsParams
from trigger import Trigger, ActionDef
from utils.get_faced_tile import get_faced_tile

PATH = os.path.abspath('.') + '/assets/'
map_definitions = MapDefinition(
    path=PATH + 'small_room.tmx',
    on_wake=[
        ActionsParams(id='add_npc', params={'def': 'strolling_npc', 'x': '11', 'y': '5'}),
        ActionsParams(id='add_npc', params={'def': 'standing_npc', 'x': '2', 'y': '5'}),
    ]
)

if __name__ == '__main__':
    if __name__ == '__main__':

        pygame.init()
        pygame.display.set_caption("jRPG Game")
        screen = pygame.display.set_mode(WINDOW_SIZE)
        display = pygame.surface.Surface(DISPLAY_SIZE)
        clock = pygame.time.Clock()

        game = Game(display=display)
        game.setup(map_definitions, ACTIONS)

        hero = Character(characters["hero"], game)

        teleport_to_bottom_door = teleport(game, 10, 12)
        trigger_at_up_door = Trigger(ActionDef(
            on_enter=teleport_to_bottom_door
        ))
        trigger_at_snake = Trigger(ActionDef(
            on_use=teleport_to_bottom_door
        ))

        game.triggers = {
            '11,3': trigger_at_up_door,
            '11,6': trigger_at_snake,
        }

        game.follow = hero.entity

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        tile_x, tile_y = get_faced_tile(hero)
                        trigger = game.get_trigger_at_tile(tile_x, tile_y)
                        if trigger is not None:
                            trigger.on_use(None, hero.entity)

            # Game Render
            screen.fill((0, 0, 0))
            display.fill((0, 0, 0))
            game.render()
            game.update()
            hero.controller.update()

            # Scale and draw the game_surface onto the screen
            surf = pygame.transform.scale(display, WINDOW_SIZE)
            screen.blit(surf, (0, 0))
            pygame.display.update()
            clock.tick(FPS)
