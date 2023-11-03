from typing import List, Tuple

import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIWindow, UIButton

from .select_item import SelectItem


class Selections(pygame_gui.elements.UIPanel):
    def __init__(self, title: str, options: List[str], columns: int, position: Tuple[float, float], manager: UIManager,
                 container: UIWindow = None):
        # Call the parent class' init method
        super().__init__(
            relative_rect=pygame.Rect(position, (300, len(options) * 50 + 50)),
            # Width and height depend on the content and style
            starting_height=1,
            manager=manager,
            container=container
        )

        # Create a title label
        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (300, 50)),
            text=title,
            manager=manager,
            container=self
        )

        self.options = options
        self.select_items: List[SelectItem] = []
        self.selection = None
        self.current_selection_idx = 0

        for idx, option in enumerate(options):
            btn = SelectItem(
                relative_rect=pygame.Rect((0, (idx + 1) * 25), (100, 25)),
                text=option,
                manager=manager,
                container=self
            )
            btn.user_data = option  # Store the option name in user_data
            self.select_items.append(btn)
        if self.select_items:
            self.select_items[self.current_selection_idx].highlight()
        self.manager = manager

    def process_events(self, event):
        for item in self.select_items:
            item.handle_event(event)
            if item.is_active:  # If the item is active
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
        self.select_items[idx].active = False

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
