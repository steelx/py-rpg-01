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

    def add_text(self, x: int, y: int, width: int, height: int, text: str):
        label = pygame_gui.elements.UILabel(
            pygame.Rect((x, y), (width, height)),
            text,
            manager=self.ui_manager,
            container=self
        )
        return label

    def add_button(self, x: int, y: int, width: int, height: int, text: str):
        button = pygame_gui.elements.UIButton(
            pygame.Rect((x, y), (width, height)),
            text,
            manager=self.ui_manager,
            container=self
        )
        return button

    def add_image(self, image_path: str, pos: Tuple[int, int] = (5, 5), size: Tuple[int, int] = (100, 100)):
        image_surface = pygame.image.load(image_path).convert_alpha()
        # size = (size[0], self.rect.height - 10)
        image_surface = pygame.transform.scale(image_surface, size)
        avatar = pygame_gui.elements.UIImage(
            pygame.Rect(pos, size),
            image_surface,
            manager=self.ui_manager,
            container=self
        )
        return avatar

    def add_title_and_message(self, title: str, message: str, pos: Tuple[int, int] = (110, 10), size: Tuple[int, int] = (200, 30)):
        title_label = pygame_gui.elements.UILabel(
            pygame.Rect(pos, size),
            title,
            manager=self.ui_manager,
            container=self,
            object_id='@text_title'
        )

        text_box = pygame_gui.elements.UITextBox(
            message,
            pygame.Rect((110, 50), (300, 50)),
            manager=self.ui_manager,
            container=self,
            object_id='@text_message'
        )

        return title_label, text_box

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
