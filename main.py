import sys

import pygame
import pygame_gui

from actions import ACTIONS
from character import Character
from character_definitions import characters
from game import Game
from globals import FPS, WINDOW_SIZE, DISPLAY_SIZE
from map_definitions import small_room_map_def
from ui import Panel
from utils import get_faced_tile

if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption("jRPG Game")
    screen = pygame.display.set_mode(WINDOW_SIZE)
    display = pygame.surface.Surface(DISPLAY_SIZE)

    game = Game(display=display)
    game.setup(small_room_map_def, ACTIONS)

    hero = Character(characters["hero"], game)
    game.follow = hero.entity

    # UI Setup
    ui_manager = pygame_gui.UIManager(WINDOW_SIZE, 'data/themes/theme.json')

    root_panel = Panel(50, 50, 400, 300, manager=ui_manager, window_display_title="Root Panel")
    # Add a child panel to the root panel
    child_panel = root_panel.add_panel(50, 50, 150, 100)

    # Add text and a button to the child panel
    child_panel.add_text(10, 10, 100, 20, "Hello")
    child_panel.add_button(10, 40, 100, 20, "Click Me")

    # Add avatar, hero name, text and action buttons
    bottom_panel_height = int(0.25 * 600)
    bottom_panel = Panel(0, 600 - bottom_panel_height, 800, bottom_panel_height, manager=ui_manager)
    bottom_panel.add_image('assets/hero_portrait.png')
    bottom_panel.add_title_and_message('Hero Name', 'This is a text message.')

    clock = pygame.time.Clock()
    while True:
        game.dt = clock.tick(FPS)
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

            # Handle UI events
            # if event.type == pygame_gui.UI_BUTTON_PRESSED:
            #     if event.ui_element == hello_button:
            #         print('Hello World!')
            ui_manager.process_events(event)

        # Game Render
        screen.fill((0, 0, 0))
        display.fill((0, 0, 0))
        ui_manager.update(game.dt)
        hero.controller.update(game.dt)
        game.update()
        game.render()

        # Scale and draw the game_surface onto the screen
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        ui_manager.draw_ui(screen)
        pygame.display.flip()
