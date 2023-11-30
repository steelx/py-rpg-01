"""
The ExploreState displays a map and lets us wander around it. The
state requires Enter, Exit, Render and Update functions. Since we’re using it with a
StateStack, and want to restrict the input, we’ll need a HandleInput function too.
"""
from typing import Tuple

import pygame
import pygame_gui

from actions import ACTIONS
from character import Character
from character_definitions import characters
from game import Game
from map_definitions import MapDefinition
from state_stack import StateStack
from world import World


class ExploreState:
    should_exit = False

    def __init__(self, map_def: MapDefinition, start_tile_pos: Tuple[int, int], display: pygame.Surface,
                 manager: pygame_gui.UIManager, stack: StateStack = None):
        self.stack = stack
        self.map_def = map_def
        self.start_pos = start_tile_pos
        self.game = Game(display=display, manager=manager, stack=stack)
        self.game.setup(map_def, ACTIONS)
        self.game.world = World(display)
        self.hero = Character(characters["hero"], self.game)
        self.hero.entity.set_tile_pos(*start_tile_pos, self.game)
        self.game.camera.set_follow(self.hero.entity)
        self.manager = manager
        self.display = display

    def hide_hero(self, hide: bool):
        self.hero.entity.visible = not hide

    def enter(self, **kwargs) -> None:
        pass

    def exit(self) -> None:
        pass

    def update(self, dt: float) -> None:
        self.game.dt = dt
        if self.hero.entity.visible:
            self.hero.controller.update(dt)
        self.game.update(dt)

    def render(self, display) -> None:
        self.game.render()

    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tile_x, tile_y = self.hero.get_faced_tile()
                trigger = self.game.get_trigger_at_tile(tile_x, tile_y)
                if trigger is not None:
                    trigger.on_use(None, self.hero.entity)
            if event.key == pygame.K_ESCAPE:
                from ingame_menu_state import InGameMenuState
                if isinstance(self.stack.top(), InGameMenuState):
                    return
                self.stack.push(
                    InGameMenuState(self.game.world, self.display, self.manager, self.stack)
                )

