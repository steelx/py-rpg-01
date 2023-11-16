import pygame
import pygame_gui

from state_stack import StackInterface
from ui import Selections, create_textbox, create_title
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
            options=self.parent.menu_options,
            position=menu_pos,
            width=self.layout.panels["menu"].width,
            columns=1,
            manager=manager,
            end_callback=self._on_selection
        )

        gold_panel = self.layout.panels["gold"]
        self.gold_points = create_textbox(
            html_text=f"""Gold Points: {menu_pos}<br>Time Played: 0:00
            """,
            pos=(self.layout.left("gold"), self.layout.top("gold")),
            size=(gold_panel.width, gold_panel.height),
            manager=self.manager,
            container=self.layout,
        )
        top_size = (self.layout.panels["top"].width, self.layout.panels["top"].height)
        self.title = create_title(
            html_text="Final Fantasy",
            pos=(self.layout.left("top")+top_size[0]*0.02, self.layout.mid_y("top")-20),
            size=top_size,
            manager=self.manager,
            container=self.layout,
        )

    def _on_selection(self, selection: str) -> None:
        if selection == "Exit":
            self.close_menu()
        else:
            self.parent.state_machine.change(selection.lower())

    def close_menu(self) -> None:
        self.layout.kill_layout()
        self.parent.should_exit = True

    def enter(self) -> None:
        self.layout.show_layout()

    def exit(self) -> None:
        self.layout.hide_layout()

    def render(self) -> None:
        self.layout.render()

    def update(self, dt) -> None:
        pass

    def process_event(self, event: pygame.event.Event):
        self.selections.process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close_menu()
