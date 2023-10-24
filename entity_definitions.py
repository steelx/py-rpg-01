import os
from dataclasses import dataclass
from typing import Dict, Tuple

from entity import EntityDefinition


PATH = os.path.abspath('.') + '/assets/'


@dataclass
class AnimationData:
    up: Tuple[int, ...]
    right: Tuple[int, ...]
    down: Tuple[int, ...]
    left: Tuple[int, ...]


@dataclass
class CharacterDefData:
    entity: str
    facing: str
    anim: AnimationData
    controller: Tuple[str, ...]
    state: str

    def __post_init__(self):
        assert self.state in self.controller, f"'{self.state}' is not a valid state in controller {self.controller}"


entities = {
    "hero": EntityDefinition(
        tile_x=9,
        tile_y=5,
        start_frame=8,
        height=24,
        width=16,
        texture_path=PATH + 'walk_cycle.png'
    )
}

# character_def
characters: Dict[str, CharacterDefData] = {
    "hero": CharacterDefData(
        entity="hero",
        facing="down",
        anim=AnimationData(
            up=(0, 1, 2, 3),
            right=(4, 5, 6, 7),
            down=(8, 9, 10, 11),
            left=(12, 13, 14, 15)
        ),
        controller=("wait", "move"),
        state="wait"
    )
}
