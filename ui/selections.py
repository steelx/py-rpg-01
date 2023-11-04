from typing import List, Tuple, Callable

import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIWindow

from .panel import Panel
from .select_item import SelectItem

LINE_HEIGHT = 25


class Selections(pygame_gui.elements.UIPanel):
    def __init__(self, title: str, options: List[str], columns: int, position: Tuple[float, float], width: int,
                 manager: UIManager,
                 container: UIWindow = None, show_info_popup: bool = False, on_selection: Callable = None):
        # Call the parent class' init method
        super().__init__(
            relative_rect=pygame.Rect(position, (width, len(options) * LINE_HEIGHT + 50)),
            starting_height=1,
            manager=manager,
            container=container
        )

        self._on_selection = on_selection
        self.elements = []
        self.options = options
        self.selection = None
        self.current_selection_idx = 0

        # Create a title label
        title_rect = pygame.Rect((0, 0), (width, 50))
        self.title = pygame_gui.elements.UILabel(
            relative_rect=title_rect,
            text=title,
            manager=manager,
            container=self,
            object_id='@text_title'
        )
        self.elements.append(self.title)

        # select items columns
        self.select_items: List[SelectItem] = []
        start_y = self.title.relative_rect.bottom
        rows_per_column = len(options) // columns + (len(options) % columns > 0)
        for idx, option in enumerate(options):
            column = idx // rows_per_column
            row = idx % rows_per_column

            item_x = column * (width / columns)
            item_y = start_y + (row * LINE_HEIGHT)

            item = SelectItem(
                relative_rect=pygame.Rect((item_x, item_y), ((width - 20) / columns, LINE_HEIGHT)),
                text=option,
                manager=manager,
                container=self
            )
            item.user_data = option
            self.select_items.append(item)
            self.elements.append(item)

        if self.select_items:
            self.select_items[self.current_selection_idx].highlight()
        self.manager = manager

        self.info_popup = None
        if show_info_popup:
            self.show_info_popup()

    def change_selection(self, change):
        if self.selection is None:
            idx = 0
        else:
            idx = self.options.index(self.selection)

        # Unhighlight current selection and deactivate it
        self.select_items[idx].unhighlight()
        self.select_items[idx].is_active = False

        idx = (idx + change) % len(self.options)
        self.selection = self.options[idx]

        # Highlight new selection
        self.select_items[idx].highlight()

    def handle_on_selection(self, user_data):
        self.selection = user_data
        if self._on_selection:
            self._on_selection(user_data)
        print(f"Selected: {self.selection}")
        self.kill()

    def get_selection(self):
        return self.selection

    def show_info_popup(self):
        popup_pos = (self.rect.x + self.rect.width, self.rect.y)
        p = Panel(popup_pos[0], popup_pos[1], 220, 200, self.manager)
        self.info_popup = p.create_textbox(
            "Use UP DOWN arrow keys to navigate. or mouse click on the item.",
            (10, 10),
            (200, 100),
            wrap_to_height=True,
            visible=False
        )
        self.select_items.append(self.info_popup)

    def update(self, dt: float):
        pass

    def render(self):
        pass

    def enter(self):
        self.visible = True
        for child in self.elements:
            child.visible = True

    def exit(self):
        self.visible = False
        for child in self.elements:
            child.visible = False

    def process_event(self, event: pygame.event.Event):
        for item in self.select_items:
            item.is_active = False
            item.handle_event(event)
            if item.is_active:
                self.handle_on_selection(item.user_data)
                break
        super().process_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Move selection up
                self.change_selection(-1)
            elif event.key == pygame.K_DOWN:
                # Move selection down
                self.change_selection(1)
            elif event.key == pygame.K_RETURN:
                # Confirm selection with Enter key
                if self.selection:
                    self.handle_on_selection(self.selection)
