import sys

import pygame
import pygame_gui

from explore_state import ExploreState
from globals import FPS, NATURAL_SIZE, ASSETS_PATH, DATA_PATH
from map_definitions import small_room_map_def
from state_stack import StateStack
from storyboard import Storyboard, fade_screen, black_screen, Wait, caption, remove_state
from ui import DialoguePanel, Textbox


def load_custom_font():
    font_path = ASSETS_PATH + "fonts/BigBlueTerm437NerdFontMono-Regular.ttf"
    font_size = 12
    return pygame.font.Font(font_path, font_size)


def main():
    pygame.init()
    big_blue_12 = load_custom_font()

    pygame.display.set_caption("jRPG Game")
    # screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen_size = (1200, 800)
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    display = pygame.surface.Surface(NATURAL_SIZE)

    # Add avatar, hero name, text and action buttons
    hero_image_path = ASSETS_PATH + "hero_portrait.png"
    message = '''A nation can survive its fools, and even the ambitious.
    But it cannot survive treason from within. An enemy at the gates is less formidable, for he is
    known and carries his banner openly. But the traitor moves amongst those
    within the gate freely, his sly whispers rustling through all the alleys, heard
    in the very halls of government itself.'''

    stack = StateStack(pygame_gui.UIManager(screen.get_size(), DATA_PATH + "themes/theme.json"))
    explore_state = ExploreState(
        stack=stack,
        map_def=small_room_map_def,
        start_tile_pos=(9, 9),
        display=display,
        manager=stack.manager
    )
    hero_pos = explore_state.game.get_hero_pos_for_ui()
    hero_pos = (hero_pos[0], hero_pos[1] - 32)

    stack.push(explore_state)
    stack.push(
        Textbox("what is this place!", hero_pos, manager=stack.manager, chars_per_line=19, lines_per_chunk=1)
    )

    storyboard = Storyboard(stack=stack, display=display, font=big_blue_12, events=[
        black_screen("black_screen"),

        caption("title_text", "title", "Village of Bavdhan", font=big_blue_12),
        fade_screen("fade_out", alpha_end=0, alpha_start=255, duration=2.0, renderer=display),
        Wait(2.0),
        remove_state("title_text"),

        caption("subtitle_text", "subtitle", "Role playing game", font=big_blue_12),
        fade_screen("fade_out", alpha_end=0, alpha_start=255, duration=2.0, renderer=display),
        Wait(2.0),
        remove_state("subtitle_text"),

        fade_screen("fade_in", alpha_end=255, alpha_start=0, duration=2.0, renderer=display),
        caption("mid_text", "default", "MIDNIGHT", font=big_blue_12),
        Wait(2),
        remove_state("mid_text"),

        remove_state("black_screen"),
    ])
    stack.push(storyboard)

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
                            manager=stack.manager,
                            end_callback=lambda: print("Dialogue ended")
                        )
                    )
                if event.key == pygame.K_q:
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
