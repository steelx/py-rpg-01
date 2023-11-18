import os
from dataclasses import dataclass
from typing import Dict, Tuple, Union

from entity import EntityDefinition

PATH = os.path.abspath('.') + '/assets/'


@dataclass
class AnimationData:
    up: Union[Tuple[int, ...], None] = None
    right: Union[Tuple[int, ...], None] = None
    down: Union[Tuple[int, ...], None] = None
    left: Union[Tuple[int, ...], None] = None


@dataclass
class CharacterDefData:
    entity: str
    facing: str
    anim: AnimationData | None
    controller: Tuple[str, ...]
    state: str

    def __post_init__(self):
        assert self.state in self.controller, f"'{self.state}' is not a valid state in controller {self.controller}"


entities = {
    "hero": EntityDefinition(
        tile_x=9,
        tile_y=5,
        rows=9,
        columns=16,
        start_frame=8,
        height=24,
        width=16,
        texture_path=PATH + 'walk_cycle.png'
    ),
    "girl": EntityDefinition(
        tile_x=9,
        tile_y=5,
        rows=9,
        columns=16,
        start_frame=24,
        height=24,
        width=16,
        texture_path=PATH + 'walk_cycle.png'
    ),
    "mage": EntityDefinition(
        tile_x=9,
        tile_y=5,
        rows=9,
        columns=16,
        start_frame=48,
        height=24,
        width=16,
        texture_path=PATH + 'walk_cycle.png'
    ),
    # sleeping zzZ sprite
    "sleeping": EntityDefinition(
        tile_x=22,
        tile_y=16,
        rows=1,
        columns=4,
        start_frame=0,
        height=32,
        width=32,
        texture_path=PATH + 'sleeping.png'
    )
}

# character_def
characters: Dict[str, CharacterDefData] = {
    "hero": CharacterDefData(
        entity="hero",
        facing="down",
        # AnimationData for the Entity hero walk-cycle
        anim=AnimationData(
            up=(0, 1, 2, 3),
            right=(4, 5, 6, 7),
            down=(8, 9, 10, 11),
            left=(12, 13, 14, 15)
        ),
        controller=("wait", "move"),
        state="wait"
    ),
    "sleeper": CharacterDefData(
        entity="hero",
        facing="left",
        anim=AnimationData(
            left=(13,)
        ),
        controller=("sleep",),
        state="sleep"
    ),
    "strolling_npc": CharacterDefData(
        entity="girl",
        facing="down",
        anim=AnimationData(
            up=(16, 17, 18, 19),
            right=(20, 21, 22, 23),
            down=(24, 25, 26, 27),
            left=(28, 29, 30, 31)
        ),
        controller=("plan_stroll", "move"),
        state="plan_stroll"
    ),
    "standing_npc": CharacterDefData(
        entity="mage",
        facing="up",
        anim=None,
        controller=("npc_stand",),
        state="npc_stand"
    )
}
