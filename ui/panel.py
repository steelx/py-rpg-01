from typing import Tuple, List

import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIWindow, UIButton, UITextBox


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

    def create_textbox(self, text: str, pos: Tuple[int, int], size: Tuple[int, int], **kwargs) -> UITextBox:
        return UITextBox(
            html_text=text,
            relative_rect=pygame.Rect(pos, size),
            starting_height=2,
            manager=self.ui_manager,
            container=self,
            object_id='@text_message',
            **kwargs
        )

    def create_button(self, x: int, y: int, width: int, height: int, text: str) -> UIButton:
        return UIButton(
            pygame.Rect((x, y), (width, height)),
            text,
            manager=self.ui_manager,
            container=self
        )

    def create_action_buttons(self, icons: List[str]) -> List[UIButton]:
        x_offset = self.rect.width - 100
        y_offset = 10
        buttons: List[UIButton] = []
        for icon_path in icons:
            icon_surface = pygame.image.load(icon_path)
            icon_surface = pygame.transform.scale(icon_surface, (30, 30))
            button = UIButton(
                pygame.Rect((x_offset, y_offset), (30, 30)),
                '',
                manager=self.ui_manager,
                container=self
            )
            button.set_text(icon_surface)
            buttons.append(button)
            y_offset += 40

        return buttons
