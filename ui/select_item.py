from typing import Tuple

import pygame
from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.elements import UILabel, UIImage
from pygame_gui.core import IContainerLikeInterface


class SelectItem(UILabel):
    def __init__(self, relative_rect: Rect, text: str,
                 manager: UIManager, container: IContainerLikeInterface = None,
                 icon_img: pygame.Surface = None, icon_size: Tuple[int, int] = (18, 18),
                 base_color=(255, 255, 255), highlight_color=(204, 255, 0), active_color=(255, 0, 0)):

        # Initialize the UILabel parent class
        self.parent = container
        super().__init__(relative_rect, text, manager, self.parent)

        self.base_color = base_color
        self.highlight_color = highlight_color
        self.active_color = active_color
        self.is_highlighted = False
        self.is_active = False
        self.update_colors()

        if icon_img is not None:
            self.icon_surf = icon_img.convert_alpha()
            pos = (relative_rect.x-icon_size[0], relative_rect.y)
            self.icon = UIImage(
                relative_rect=Rect(pos, icon_size),
                image_surface=self.icon_surf,
                manager=manager,
                container=self.parent,
                parent_element=self.parent
            )

    def update_colors(self):
        if self.is_active:
            self.text_colour = self.active_color
        elif self.is_highlighted:
            self.text_colour = self.highlight_color
        else:
            self.text_colour = self.base_color
        self.rebuild()

    def highlight(self):
        self.is_highlighted = True
        self.update_colors()

    def unhighlight(self):
        self.is_highlighted = False
        self.update_colors()

    def set_active(self):
        self.is_active = True
        self.update_colors()

    def deactivate(self):
        self.is_active = False
        self.update_colors()

    def handle_event(self, event):
        # Check for mouse hover
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.highlight()
            else:
                self.unhighlight()

        # Check for mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.on_select()

    def on_select(self):
        self.set_active()
