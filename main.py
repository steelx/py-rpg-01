import sys

import pygame
import pygame_gui

from actions import ACTIONS
from character import Character
from character_definitions import characters
from game import Game
from globals import FPS, WINDOW_SIZE, DISPLAY_SIZE
from map_definitions import small_room_map_def
from ui import DialoguePanel
from utils import get_faced_tile

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
    ui_manager = pygame_gui.UIManager(WINDOW_SIZE, 'data/themes/theme.json')

    # Add avatar, hero name, text and action buttons
    hero_image_path = 'assets/hero_portrait.png'
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

if __name__ == '__main__':
    main()
