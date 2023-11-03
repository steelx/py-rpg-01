from typing import List, Tuple

import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIWindow

from .panel import Panel
from .select_item import SelectItem

LINE_HEIGHT = 25


class Selections(pygame_gui.elements.UIPanel):
    def __init__(self, title: str, options: List[str], columns: int, position: Tuple[float, float], width: int, manager: UIManager,
                 container: UIWindow = None, show_info_popup: bool = False):
        # Call the parent class' init method
        super().__init__(
            relative_rect=pygame.Rect(position, (width, len(options) * LINE_HEIGHT + 50)),
            starting_height=1,
            manager=manager,
            container=container
        )

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
                relative_rect=pygame.Rect((item_x, item_y), ((width-20) / columns, LINE_HEIGHT)),
                text=option,
                manager=manager,
                container=self
            )
            item.user_data = option
            self.select_items.append(item)

        if self.select_items:
            self.select_items[self.current_selection_idx].highlight()
        self.manager = manager

        self.info_popup = None
        if show_info_popup:
            self.show_info_popup()

    def process_events(self, event):
        for item in self.select_items:
            item.is_active = False
            item.handle_event(event)
            if item.is_active:
                self.on_selection(item.user_data)
                break

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
                    self.on_selection(self.selection)

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

    def on_selection(self, user_data):
        self.selection = user_data
        # This method will be called when a selection is made
        # You can override this in a subclass or replace this method with another action
        print(f"Selected: {self.selection}")

    def get_selection(self):
        return self.selection

    def show_info_popup(self):
        popup_pos = (self.rect.x + self.rect.width, self.rect.y)
        self.info_popup = Panel(popup_pos[0], popup_pos[1], 220, 200, self.manager)
        self.info_popup.add_text(
            "Use UP DOWN arrow keys to navigate. or mouse click on the item.",
            (10, 10),
            (200, 100),
            wrap_to_height=True
        )
