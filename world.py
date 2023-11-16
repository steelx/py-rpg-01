"""
World object tracks all the items the party picks up, the amount of gold they have,
and the amount of time that has passed. Later on it will also track quests and current
party members, and be involved with loading and saving.
"""
from typing import TypedDict, List, Any, Dict

import pygame
from pygame_gui import UIManager
from pygame_gui.core import IContainerLikeInterface

from globals import ASSETS_PATH
from items import item_db
from ui import Icons, SelectItem


class InventoryItem(TypedDict):
    id: int  # The ID which should reference an item in item_db
    count: int


class World:
    should_exit = False
    items: List[InventoryItem]
    key_items: List[InventoryItem]

    def __init__(self, renderer: pygame.Surface):
        self.renderer = renderer
        self.time = 0
        self.gold = 0
        self.items = [
            {"id": 1, "count": 2},
            {"id": 0, "count": 1},
            {"id": 2, "count": 1},
        ]
        self.key_items = [
            {"id": 3, "count": 1},
        ]
        self.icons = Icons(ASSETS_PATH + "ui/inventory_icons.png")

    def update(self, dt: float) -> None:
        self.time += dt

    def add_item(self, item_id: int, count: int = 1) -> None:
        """
        Add an item to the inventory. else, increase the count of the item if it already exists.
        & making sure it's not a Category.KEY item
        """
        assert item_db[item_id].category != "key", f"Cannot add key item to inventory: {item_db[item_id]}"
        for item in self.items:
            if item["id"] == item_id:
                item["count"] += count
                return
        self.items.append({"id": item_id, "count": count})

    def remove_item(self, item_id: int, count: int = 1) -> None:
        """
        Remove an item from the inventory. If the count of the item is 0, remove it from the inventory
        """
        for item in self.items:
            if item["id"] == item_id:
                item["count"] -= count
                if item["count"] <= 0:
                    self.items.remove(item)
                return
        assert False, f"Item {item_id} not found in inventory"

    def has_key_item(self, item_id: int) -> bool:
        """
        Check if the player has a key item
        """
        for item in self.key_items:
            if item["id"] == item_id:
                return True
        return False

    def add_key_item(self, item_id: int) -> None:
        """
        Add a key item to the inventory, you can never have more than one type of key item
        """
        assert item_db[item_id].category == "key", f"Cannot add non-key item to key items: {item_db[item_id]}"
        assert not self.has_key_item(item_id), f"Cannot add duplicate key item: {item_db[item_id]}"
        for item in self.key_items:
            if item["id"] == item_id:
                return
        self.key_items.append({"id": item_id, "count": 1})

    def remove_key_item(self, item_id: int) -> None:
        """
        Remove a key item from the key_items
        """
        assert item_db[item_id].category != "key", f"Cannot remove non-key item from key items: {item_db[item_id]}"
        for item in self.key_items:
            if item["id"] == item_id:
                self.key_items.remove(item)
                return
        assert False, f"Key item {item_id} not found in inventory"

    def time_as_string(self) -> str:
        hours = int(self.time // 3600)
        minutes = int(self.time // 60)
        seconds = int(self.time % 60)
        return f"{hours}::{minutes}:{seconds:02}"

    def draw_item(self, item: Dict[str, Any], x: float, y: float, manager: UIManager,  container: IContainerLikeInterface) -> SelectItem:
        assert "id" in item, f"Item {item} does not have an id"
        assert "count" in item, f"Item {item} does not have a count"
        item_id = item["id"]
        count = item["count"]
        item_def = item_db[item_id]
        icon = self.icons.get_icon(item_def.category.name.lower())
        icon_w = 18
        text_w = len(item_def.name) * 10 + icon_w
        return SelectItem(
            relative_rect=pygame.Rect((x+icon_w+5, y), (text_w, 25)),
            text=f"{item_def.name} x{count}",
            manager=manager,
            container=container,
            icon_img=icon,
            icon_size=(icon_w, icon_w)
        )


