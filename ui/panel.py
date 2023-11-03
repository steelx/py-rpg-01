from typing import Tuple

import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIWindow


class Panel(UIWindow):
    def __init__(self, x: int, y: int, width: int, height: int, manager: UIManager, **kwargs):
        super().__init__(
            pygame.Rect((x, y), (width, height)),
            manager=manager,
            draggable=False,
            **kwargs
        )

        self.grid = []

    def add_panel(self, x: int, y: int, width: int, height: int):
        child_panel = Panel(x, y, width, height, self.ui_manager)
        self.grid.append(child_panel)
        return child_panel

    def add_text(self, text: str, pos: Tuple[int, int], size: Tuple[int, int], **kwargs):
        pygame_gui.elements.UITextBox(
            html_text=text,
            relative_rect=pygame.Rect(pos, size),
            starting_height=2,
            manager=self.ui_manager,
            container=self,
            object_id='@text_message',
            **kwargs
        )

    def add_button(self, x: int, y: int, width: int, height: int, text: str):
        button = pygame_gui.elements.UIButton(
            pygame.Rect((x, y), (width, height)),
            text,
            manager=self.ui_manager,
            container=self
        )
        return button

    def add_action_buttons(self, icons: list):
        x_offset = self.rect.width - 100
        y_offset = 10
        buttons = []
        for icon_path in icons:
            icon_surface = pygame.image.load(icon_path)
            icon_surface = pygame.transform.scale(icon_surface, (30, 30))
            button = pygame_gui.elements.UIButton(
                pygame.Rect((x_offset, y_offset), (30, 30)),
                '',
                manager=self.ui_manager,
                container=self
            )
            button.set_text(icon_surface)
            buttons.append(button)
            y_offset += 40

        return buttons
