import sys

import pygame
import pygame_gui

from actions import ACTIONS
from character import Character
from character_definitions import characters
from game import Game
from globals import FPS, WINDOW_SIZE, DISPLAY_SIZE, ASSETS_PATH, DATA_PATH
from map_definitions import small_room_map_def
from state_stack import StateStack
from ui import DialoguePanel, Selections, Textbox
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
    in the very halls of government itself.'''

    dialog_panel = DialoguePanel(hero_image_path, "Hero", message, ui_manager, WINDOW_SIZE)
    selections = Selections(
        "Yes or no",
        ["YES", "NO"],
        2, (100, 200), 150,
        manager=ui_manager)
    text_box = Textbox("""A nation can survive its fools, and even the ambitious.
    But it cannot survive treason from within. An enemy at the gates is less formidable, for he is
    known and carries his banner openly.""", (0, 0), (150, 100), chars_per_line=15, lines_per_chunk=3, manager=ui_manager)

    state_stack = StateStack(ui_manager)
    state_stack.push(selections)
    state_stack.push(text_box)
    state_stack.push(dialog_panel)

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
            # State Stack Event Handling
            state_stack.process_event(event)

        # Game Render
        screen.fill((0, 0, 0))
        display.fill((0, 0, 0))
        hero.controller.update(game.dt)
        game.update()
        game.render()
        state_stack.update(game.dt)

        # Scale and draw the game_surface onto the screen
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        state_stack.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
