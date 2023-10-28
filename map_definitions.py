import os
from dataclasses import dataclass
from typing import List, Union, Any, Optional, Dict

@dataclass
class ActionsParams:
    id: str
    params: dict[str, Union[int, str, Any]] # def = "strolling_npc", x = 11, y = 5

@dataclass
class TriggerType:
    on_enter: str = None
    on_exit: str = None
    on_use: str = None

@dataclass
class TriggerData:
    trigger: str
    x: int
    y: int

@dataclass
class MapDefinition:
    path: str
    on_wake: List[ActionsParams] = None
    actions: Optional[Dict[str, ActionsParams]] = None
    triggers_type: Optional[Dict[str, Dict[str, str]]] = None
    triggers_at_tile: Optional[List[TriggerData]] = None


PATH = os.path.abspath('.') + '/assets/'
map_definitions = MapDefinition(
    path=PATH + 'small_room.tmx',
    on_wake=[
        ActionsParams(id='add_npc', params={'def': 'strolling_npc', 'x': 11, 'y': 5}),
        ActionsParams(id='add_npc', params={'def': 'standing_npc', 'x': 2, 'y': 5}),
    ],
    actions={
        'teleport_south': ActionsParams(id='teleport', params={'tile_x': 10, 'tile_y': 11}),
        'teleport_north': ActionsParams(id='teleport', params={'tile_x': 11, 'tile_y': 4}),
        'teleport_inside_true': ActionsParams(id='teleport', params={'tile_x': 7, 'tile_y': 7}),
    },
    triggers_type={
        'north_door_trigger': {'on_enter': 'teleport_south'},
        'south_door_trigger': {'on_enter': 'teleport_north'},
        'snake': {'on_use': 'teleport_inside_true'},
    },
    triggers_at_tile=[
        TriggerData(trigger='north_door_trigger', x=11, y=3),
        TriggerData(trigger='south_door_trigger', x=10, y=12),
        TriggerData(trigger='snake', x=11, y=6),
    ]
)
