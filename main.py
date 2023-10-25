import os
import sys

import pygame

from actions import teleport
from character import Character
from character_definitions import characters
from game import Game
from globals import FPS, WINDOW_SIZE, DISPLAY_SIZE
from trigger import Trigger, ActionDef
from utils import get_faced_tile

PATH = os.path.abspath('.') + '/assets/'

if __name__ == '__main__':
    if __name__ == '__main__':
        
        pygame.init()
        pygame.display.set_caption("jRPG Game")
        screen = pygame.display.set_mode(WINDOW_SIZE)
        display = pygame.surface.Surface(DISPLAY_SIZE)
        clock = pygame.time.Clock()

        game = Game(PATH + 'small_room.tmx', display=display)
        game.build_map()

        hero = Character(characters["hero"], game)
        standing_npc = Character(characters["standing_npc"], game)
        teleport(game, 2, 6)(None, standing_npc.entity)

        strolling_npc = Character(characters["strolling_npc"], game)

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
            standing_npc.controller.update()
            strolling_npc.controller.update()

            # Scale and draw the game_surface onto the screen
            surf = pygame.transform.scale(display, WINDOW_SIZE)
            screen.blit(surf, (0, 0))
            pygame.display.update()
            clock.tick(FPS)
