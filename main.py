import sys

import pygame
import pygame_gui

from actions import ACTIONS
from character import Character
from character_definitions import characters
from game import Game
from globals import FPS, WINDOW_SIZE, DISPLAY_SIZE
from map_definitions import small_room_map_def
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
    ui_manager = pygame_gui.UIManager(WINDOW_SIZE, 'gui_theme.json')

    panel_layout_rect = pygame.display.get_surface().get_rect().inflate(-50, -50)
    panel = pygame_gui.elements.UIPanel(relative_rect=panel_layout_rect, manager=ui_manager)

    pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(30, 20, 100, 50),
        text='Hello 1',
        manager=ui_manager,
        container=panel)
    button_rect = pygame.Rect(100, 100, 100, 50)
    hello_button = pygame_gui.elements.UIButton(
        relative_rect=button_rect,
        text='Say Hello',
        manager=ui_manager, container=panel,
        anchors={'left': 'left',
                 'right': 'right',
                 'top': 'top',
                 'bottom': 'bottom'}
    )

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
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    print('Hello World!')
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
