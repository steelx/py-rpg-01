import pygame
import pygame_gui

from state_stack import StackInterface
from ui import Selections
from ui.layout import Layout


class FrontMenuState:
    def __init__(self, parent: StackInterface, manager: pygame_gui.UIManager, display: pygame.Surface):
        from ingame_menu_state import InGameMenuState
        assert isinstance(parent, InGameMenuState)
        self.parent = parent
        self.manager = manager
        self.layout = Layout(self.manager)
        self.layout.contract("screen", 120, 60)
        self.layout.split_horz("screen", "top", "bottom", 0.2)
        self.layout.split_vert("bottom", "left", "party", 0.8)
        self.layout.split_horz("left", "menu", "gold", 0.7)
        menu_pos = (self.layout.left("menu"), self.layout.top("menu"))
        self.selections = Selections(
            container=self.layout,
            title="Select an action",
            options=[
                "Item",
                "Magic",
                "Equip",
                "Status",
                "Exit"
            ],
            position=menu_pos,
            width=self.layout.panels["menu"].width,
            columns=1,
            manager=manager,
            on_selection=self._on_selection
        )

    def _on_selection(self, selection: str) -> None:
        if selection == "Exit":
            self.close_frontmenu()

    def close_frontmenu(self) -> None:
        self.layout.kill_layout()
        self.parent.should_exit = True

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def render(self) -> None:
        self.layout.render()

    def update(self, dt) -> None:
        pass

    def process_event(self, event: pygame.event.Event):
        self.selections.process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.close_frontmenu()
