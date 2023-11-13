"""
items.py
Items are anything in the world the player can pick up. Examples include keys, swords
and health potions. All items have a few things in common. They have a name and a
description. For example, a key might be called “Rusty Key” and the description might
be “A small rusted key. What could it open?” For our purposes items fall into the
following categories:
• Key Item - a special item, usually required to progress past a certain part of the
game.
• Weapon - an item that can be equipped and has properties related to inflicting
damage.
• Armor - an item that can be equipped and has properties related to reducing
damage.
• Accessory - an item that can be equipped and has special properties.
• Usable - an item that can be used during combat or on the world map.
"""
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict
from typing import Optional


class Category(Enum):
    KEY = auto()
    WEAPON = auto()
    ARMOR = auto()
    ACCESSORY = auto()
    USABLE = auto()
    EMPTY = auto()

    def __str__(self):
        return self.name.lower()


@dataclass
class Stats:
    strength: int = 0
    speed: int = 0
    intelligence: int = 0
    attack: int = 0
    defense: int = 0
    magic: int = 0
    resist: int = 0


@dataclass
class Item:
    name: str
    description: str
    category: Category
    stats: Optional[Stats] = None
    special: str = ""


# Creating a type alias for the item database dictionary
ItemDBType = Dict[int, Item]

item_db: ItemDBType = {
    -1: Item(
        name="",
        description="",
        category=Category.EMPTY,
        stats=Stats(),
        special=""
    ),
    0: Item(
        name="Mysterious Torque",
        category=Category.ACCESSORY,
        description="A golden torque that glitters.",
        stats=Stats(strength=10, speed=10)
    ),
    1: Item(
        name="Heal Potion",
        category=Category.USABLE,
        description="Heals a little HP."
    ),
    2: Item(
        name="Bronze Sword",
        category=Category.WEAPON,
        description="A short sword with dull blade.",
        stats=Stats(attack=10)
    ),
    3: Item(
        name="Old bone",
        category=Category.KEY,
        description="A calcified human femur"
    ),
}

empty_item = item_db[-1]


# Function to determine if an item has stats based on its category
def does_item_have_stats(item_: Item) -> bool:
    return item_.category in ("weapon", "accessory", "armor")


# # Populate missing stats for items that should have stats
# for item in item_db.values():
#     if does_item_have_stats(item) and item.stats is None:
#         item.stats = Stats()
