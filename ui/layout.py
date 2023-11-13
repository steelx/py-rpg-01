from dataclasses import dataclass
from typing import Dict

import pygame
import pygame_gui


@dataclass
class PanelType:
    x: float
    y: float
    width: float
    height: float


class Layout(pygame_gui.elements.UIPanel):
    """
    the operations starting with a panel the size of the display area:
    1. Contract the panel.
    2. Horizontally cut the panel 15% from the top.
    3. Cut the lower panel vertically at 20% from the left.
    4. Cut the left panel horizontally at 80% from the top.

    We’re going to take that English language description and turn it into code to show
    how we’d like our Layout class to work. Lua is a great language for doing this kind of
    translation.

    1. layout.contract('screen', 118, 40)
    2. layout.split_horz('screen', 'upper', 'lower', 0.15)
    3. layout.split_vert('lower', 'left', 'right', 0.20)
    4. layout.split_horz('left', 'left_upper', 'left_lower', 0.8)

    """
    panels: Dict[str, PanelType | None]

    def __init__(self, manager: pygame_gui.UIManager):
        self.manager = manager
        w, h = manager.window_resolution
        super().__init__(
            relative_rect=pygame.Rect(0, 0, w, h),
            starting_height=1,
            manager=self.manager,
            object_id='@text_panel_bg'
        )
        self.panels = {}
        self.x = 0
        self.y = 0

        # First panel is the full screen
        self.panels["screen"] = PanelType(0, 0, w, h)

    def create_panel(self, panel_name: str) -> pygame_gui.elements.UIPanel:
        p = self.panels[panel_name]
        return pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(p.x, p.y, p.width, p.height),
            starting_height=1,
            manager=self.manager,
            container=self,
            object_id='@text_panel'
        )

    def kill_layout(self) -> None:
        self.kill()

    def render(self):
        for p in self.panels.keys():
            panel = self.panels[p]
            if panel is not None:
                self.create_panel(p)

    def contract(self, panel_name: str, horz: float, vert: float) -> None:
        assert panel_name in self.panels
        self.panels[panel_name].width -= horz
        self.panels[panel_name].height -= vert
        self.panels[panel_name].x += horz / 2
        self.panels[panel_name].y += vert / 2

    def split_horz(self, panel_name: str, top_name: str, bottom_name: str, split_ratio: float) -> None:
        assert panel_name in self.panels
        parent = self.panels[panel_name]
        del self.panels[panel_name]

        top_height = parent.height * split_ratio
        bottom_height = parent.height * (1 - split_ratio)
        self.panels[top_name] = PanelType(
            x=parent.x,
            y=parent.y,
            width=parent.width,
            height=top_height
        )
        self.panels[bottom_name] = PanelType(
            x=parent.x,
            y=parent.y + top_height,
            width=parent.width,
            height=bottom_height
        )

    def split_vert(self, panel_name: str, left_name: str, right_name: str, split_ratio: float) -> None:
        assert panel_name in self.panels
        parent = self.panels[panel_name]
        del self.panels[panel_name]

        left_width = parent.width * (1 - split_ratio)
        right_width = parent.width * split_ratio
        self.panels[left_name] = PanelType(
            x=parent.x,
            y=parent.y,
            width=left_width,
            height=parent.height
        )
        self.panels[right_name] = PanelType(
            x=parent.x + left_width,
            y=parent.y,
            width=right_width,
            height=parent.height
        )

    def top(self, panel_name: str) -> float:
        assert panel_name in self.panels
        return self.panels[panel_name].y

    def bottom(self, panel_name: str) -> float:
        assert panel_name in self.panels
        p = self.panels[panel_name]
        return p.y + p.height

    def left(self, panel_name: str) -> float:
        assert panel_name in self.panels
        return self.panels[panel_name].x

    def right(self, panel_name: str) -> float:
        assert panel_name in self.panels
        p = self.panels[panel_name]
        return p.x + p.width

    def mid_x(self, panel_name: str) -> float:
        assert panel_name in self.panels
        p = self.panels[panel_name]
        return p.x + p.width / 2

    def mid_y(self, panel_name: str) -> float:
        assert panel_name in self.panels
        p = self.panels[panel_name]
        return p.y + p.height / 2
