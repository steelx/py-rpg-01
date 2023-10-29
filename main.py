import sys

import pygame
import thorpy

from actions import ACTIONS
from character import Character
from character_definitions import characters
from game import Game
from globals import FPS, WINDOW_SIZE, DISPLAY_SIZE
from gui.panel import Panel
from map_definitions import small_room_map_def
from utils import get_faced_tile


if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption("jRPG Game")
    screen = pygame.display.set_mode(WINDOW_SIZE)
    display = pygame.surface.Surface(DISPLAY_SIZE)

    # GUI
    thorpy.init(screen, thorpy.theme_game1)
    check = thorpy.Labelled("Checkbox:", thorpy.Checkbox(True))
    radio = thorpy.Labelled("Radio:", thorpy.Radio(True))
    slider = thorpy.SliderWithText("Health:", 10, 80, 30, 100, edit=False)
    p1 = Panel([thorpy.Button("P1 World!"), thorpy.Button("Hello World!")], color=(255, 0, 255))
    p2 = Panel([thorpy.Button("P2 World!"), check, radio, slider], color=(0, 0, 255), size=(600, 300))
    panel = Panel([p1, p2], color=(255, 255, 0))
    panel.set_size(DISPLAY_SIZE, False)
    ui_elements = thorpy.Group([panel])
    ui_elements.center_on(screen)
    ui_updater = ui_elements.get_updater()

    # Game
    clock = pygame.time.Clock()
    game = Game(display=display)
    game.setup(small_room_map_def, ACTIONS)

    hero = Character(characters["hero"], game)
    game.follow = hero.entity

    while True:
        events = pygame.event.get()
        for event in events:
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
        hero.controller.update(game.dt)
        game.update()
        game.render()
        # Scale and draw the game_surface onto the screen
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))

        # GUI Render
        ui_updater.update(events=events)

        pygame.display.flip()
        game.dt = clock.tick(FPS)
