import sys

import pygame
import pygame_gui

from explore_state import ExploreState
from globals import FPS, NATURAL_SIZE, ASSETS_PATH, DATA_PATH
from map_definitions import small_room_map_def
from state_stack import StateStack
from storyboard import Storyboard, fade_screen, black_screen, Wait, caption, remove_state, no_blocking, play_sound, \
    stop_sound, scene
from ui import DialoguePanel


def load_custom_font(font_size=12) -> pygame.font.Font:
    font_path = ASSETS_PATH + "fonts/BigBlueTerm437NerdFontMono-Regular.ttf"
    return pygame.font.Font(font_path, font_size)


def main():
    pygame.init()
    big_blue_12 = load_custom_font()

    pygame.display.set_caption("jRPG Game")
    # screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen_size = (1200, 800)
    screen = pygame.display.set_mode(screen_size, pygame.DOUBLEBUF | pygame.HWSURFACE)
    display = pygame.surface.Surface(NATURAL_SIZE)

    # Add avatar, hero name, text and action buttons
    hero_image_path = ASSETS_PATH + "hero_portrait.png"
    message = '''A nation can survive its fools, and even the ambitious.
    But it cannot survive treason from within. An enemy at the gates is less formidable, for he is
    known and carries his banner openly. But the traitor moves amongst those
    within the gate freely, his sly whispers rustling through all the alleys, heard
    in the very halls of government itself.'''

    ui_manager = pygame_gui.UIManager(screen.get_size(), DATA_PATH + "themes/theme.json")
    stack = StateStack(ui_manager)
    explore_state = ExploreState(
        stack=stack,
        map_def=small_room_map_def,
        start_tile_pos=(9, 9),
        display=display,
        manager=stack.manager
    )
    stack.push(explore_state)

    storyboard = Storyboard(stack=stack, display=display, events=[
        black_screen("black_screen"),
        play_sound("rain", ASSETS_PATH + "sounds/rain.wav", volume=0.2),

        caption("place", "title", "Village of Bavdhan", font=load_custom_font(24)),
        fade_screen("fade_out_1", alpha_end=0, alpha_start=255, duration=2.0, renderer=display),
        caption("time", "subtitle", "MIDNIGHT", font=big_blue_12),
        Wait(2.0),
        no_blocking(
            fade_screen("fade_out_2", alpha_end=0, alpha_start=255, duration=2.0, renderer=display),
        ),
        fade_screen("fade_in", alpha_end=255, alpha_start=0, duration=2.0, renderer=display),
        remove_state("place"),
        remove_state("time"),

        caption("mid_text", "default", "Meet the hero", font=big_blue_12),
        fade_screen("fade_out_3", alpha_end=0, alpha_start=255, duration=2.0, renderer=display),
        Wait(2),
        remove_state("mid_text"),
        stop_sound("rain"),
        remove_state("black_screen"),

        no_blocking(scene("player_house", 5)),
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
        # Clear
        screen.fill((0, 0, 0))
        display.fill((0, 0, 0))
        stack.render(display)
        # Scale and draw the game_surface onto the screen
        window_size = screen.get_size()
        surf = pygame.transform.scale(display, window_size)
        screen.blit(surf, (0, 0))
        ui_manager.draw_ui(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
