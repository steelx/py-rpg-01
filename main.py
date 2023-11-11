import sys

import pygame
import pygame_gui

from explore_state import ExploreState
from fade_state import FadeState
from globals import FPS, DISPLAY_SIZE, ASSETS_PATH, DATA_PATH
from map_definitions import small_room_map_def
from state_stack import StateStack
from ui import DialoguePanel, Textbox


def main():
    pygame.init()
    pygame.display.set_caption("jRPG Game")
    # screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen_size = (1200, 800)
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    display = pygame.surface.Surface(DISPLAY_SIZE)

    # Add avatar, hero name, text and action buttons
    hero_image_path = ASSETS_PATH + "hero_portrait.png"
    message = '''A nation can survive its fools, and even the ambitious.
    But it cannot survive treason from within. An enemy at the gates is less formidable, for he is
    known and carries his banner openly. But the traitor moves amongst those
    within the gate freely, his sly whispers rustling through all the alleys, heard
    in the very halls of government itself.'''

    stack = StateStack(pygame_gui.UIManager(screen_size, DATA_PATH + "themes/theme.json"))
    explore_state = ExploreState(
        stack=None,
        map_def=small_room_map_def,
        start_tile_pos=(9, 9),
        display=display,
        manager=stack.manager
    )
    hero_pos = explore_state.game.get_hero_pos_for_ui()
    hero_pos = (hero_pos[0], hero_pos[1] - 32)

    stack.push(explore_state)
    stack.push(
        Textbox("where am I", hero_pos, manager=stack.manager, chars_per_line=10, lines_per_chunk=1)
    )
    # stack.push(FadeState({"duration": 1, "alpha_start": 255, "alpha_finish": 0}, display))
    # stack.push(
    #     Textbox("ah my head hurts", hero_pos, manager=stack.manager, chars_per_line=16, lines_per_chunk=1)
    # )

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            stack.process_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    stack.push(
                        DialoguePanel(
                            hero_image=hero_image_path,
                            hero_name="Hero",
                            message=message,
                            manager=stack.manager
                        )
                    )
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update
        stack.update(dt)

        # Render
        stack.render(screen, display)
        pygame.display.flip()


if __name__ == '__main__':
    main()
