import sys

import pygame
import pygame_gui

from actions import ACTIONS
from character import Character
from character_definitions import characters
from game import Game
from globals import FPS, WINDOW_SIZE, DISPLAY_SIZE, ASSETS_PATH, DATA_PATH
from map_definitions import small_room_map_def
from ui import DialoguePanel, Selections, ProgressBar
from utils import get_faced_tile

FONTS = [
    {"name": "BigBlueTerm437NerdFont", "point_size": 12, "style": "regular"},
    {"name": "BigBlueTerm437NerdFont", "point_size": 14, "style": "regular"},
    {"name": "BigBlueTerm437NerdFont", "point_size": 18, "style": "regular"},
    {"name": "BigBlueTerm437NerdFont", "point_size": 24, "style": "regular"},
]


def main():
    pygame.init()
    pygame.display.set_caption("jRPG Game")
    screen = pygame.display.set_mode(WINDOW_SIZE)
    display = pygame.surface.Surface(DISPLAY_SIZE)

    game = Game(display=display)
    game.setup(small_room_map_def, ACTIONS)

    hero = Character(characters["hero"], game)
    game.follow = hero.entity

    # UI Setup
    ui_manager = pygame_gui.UIManager(WINDOW_SIZE, DATA_PATH + "themes/theme.json")

    # Add avatar, hero name, text and action buttons
    hero_image_path = ASSETS_PATH + "hero_portrait.png"
    message = '''A nation can survive its fools, and even the ambitious.
But it cannot survive treason from within. An enemy at the gates is less formidable, for he is
known and carries his banner openly. But the traitor moves amongst those
within the gate freely, his sly whispers rustling through all the alleys, heard
in the very halls of government itself. For the traitor appears not a traitor;
he speaks in accents familiar to his victims, and he wears their face and
their arguments, he appeals to the baseness that lies deep in the hearts
of all men. He rots the soul of a nation, he works secretly and unknown in
the night to undermine the pillars of the city, he infects the body politic so
that it can no longer resist. A murderer is less to fear. The traitor is the
plague.'''
    bottom_panel = DialoguePanel(ui_manager, WINDOW_SIZE)
    bottom_panel.setup_dialogue(hero_image_path, "Hero", message)

    selections = Selections(
        "Yes or no",
        ["YES", "NO"],
        2, (100, 200), 150,
        manager=ui_manager, show_info_popup=False)

    # Calculate the top center of the hero, then move up by the height of the progress bar plus some padding
    hero_tile_rect = game.get_scaled_rect_for_ui(9, 5)
    health_bar = ProgressBar(
        rect=hero_tile_rect,
        manager=ui_manager,
        start_progress=10,
        object_id="@hp_progress_bar"
    )
    health_bar.set_progress(20)

    clock = pygame.time.Clock()
    while True:
        game.dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bottom_panel.show_next_chunk()
                    tile_x, tile_y = get_faced_tile(hero)
                    trigger = game.get_trigger_at_tile(tile_x, tile_y)
                    if trigger is not None:
                        trigger.on_use(None, hero.entity)

            # Handle UI events
            selections.process_events(event)
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
        health_bar.update_position(game.get_scaled_rect_for_ui(hero.entity.tile_x, hero.entity.tile_y).topleft)
        health_bar.draw()

        # Scale and draw the game_surface onto the screen
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        ui_manager.draw_ui(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
