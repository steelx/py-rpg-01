from typing import List, Tuple, Callable, Any, Dict

import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.core import IContainerLikeInterface

from .select_item import SelectItem

LINE_HEIGHT = 25


class Selections(pygame_gui.elements.UIPanel):
    def __init__(self, columns: int, position: Tuple[float, float], width: float,
                 manager: UIManager, container: IContainerLikeInterface = None,
                 title: str = None,
                 options: List[str] = None, data: List[Dict[str, Any]] = None, render_data_item: Callable = None,
                 end_callback: Callable = None):

        assert options or data, "Either options or data must be provided"
        super().__init__(
            relative_rect=pygame.Rect(position, (width, len(options or data) * LINE_HEIGHT + 50)),
            starting_height=11,
            manager=manager,
            container=container,
            object_id='@text_panel_bg'
        )
        self.manager = manager
        self.container = container
        self.should_exit = False
        self.width = width
        self.columns = columns
        self._on_selection = end_callback
        self.options = options
        self.data = data
        self.render_data_item = render_data_item
        self.selection = None
        self.current_selection_idx = 0

        self.title = title
        self.select_items: List[SelectItem] = []
        self._create_ui()

    def _create_ui(self):
        if self.title is not None:
            title_rect = pygame.Rect((0, 0), (self.width, 50))
            self.title = pygame_gui.elements.UILabel(
                relative_rect=title_rect,
                text=self.title,
                manager=self.manager,
                container=self,
                object_id='@text_title'
            )

        # select items columns
        start_y = self.title.relative_rect.bottom

        select_options = self.options or self.data
        rows_per_column = len(select_options) // self.columns + (len(select_options) % self.columns > 0)
        for idx, option in enumerate(select_options):
            column = idx // rows_per_column
            row = idx % rows_per_column

            item_x = column * (self.width / self.columns)
            item_y = start_y + (row * LINE_HEIGHT)

            item: SelectItem = (
                self.render_data_item(option, item_x, item_y, self.manager, self) if self.render_data_item
                else SelectItem(
                    relative_rect=pygame.Rect((item_x, item_y), ((self.width - 20) / self.columns, LINE_HEIGHT)),
                    text=option,
                    manager=self.manager,
                    container=self
                )
            )
            item.user_data = option
            self.select_items.append(item)

        if self.select_items:
            self.select_items[self.current_selection_idx].highlight()

    def change_selection(self, change):
        options = self.options or self.data
        if self.selection is None:
            idx = 0
        else:
            idx = options.index(self.selection)

        # Unhighlight current selection and deactivate it
        self.select_items[idx].unhighlight()
        self.select_items[idx].is_active = False

        idx = (idx + change) % len(options)
        self.selection = options[idx]

        # Highlight new selection
        self.select_items[idx].highlight()

    def handle_on_selection(self, user_data):
        self.selection = user_data
        if self._on_selection:
            self._on_selection(user_data)
        self.should_exit = True

    def get_selection(self):
        return self.selection

    def update(self, dt: float):
        pass

    def render(self):
        pass

    def enter(self):
        self.show()

    def exit(self):
        self.hide()

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
