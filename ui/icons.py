"""
The icon texture is 180x180 pixels and each icon is 18x18 pixels. Therefore, the texture
sheet can contain up to 100 icons. That’s more than enough for our needs! What we
want to do is take this texture, split it up into 18 x 18 pixels chunks, and create a sprite
for each icon we want to use. Each icon is given a simple id.

Icon Category:
    usable = 1,
    accessory = 2,
    weapon = 3,
    armor = 4,
    up_arrow = 5,
    down_arrow = 6
"""
from enum import Enum, auto
from typing import Dict

import pygame

from sprite_utils import load_sprite_sheet


class Icons:
    def __init__(self, spritesheet_path: str):
        self.spritesheet = load_sprite_sheet(spritesheet_path, 18, 18, 2, 10)
        self.icon_category = {
            "usable": 1,
            "accessory": 2,
            "weapon": 3,
            "armor": 4,
            "up_arrow": 5,
            "down_arrow": 6
        }
        self.icons: Dict[str, pygame.Surface] = {}
        self.create_icons()

    def create_icons(self):
        for category, idx in self.icon_category.items():
            self.icons[category] = self.spritesheet[idx]

    def get_icon(self, category: str) -> pygame.Surface:
        assert category in self.icons, f"Icon id {category} not found"
        return self.icons[category]
