import os
from dataclasses import dataclass
from typing import List, Union, Any, Optional, Dict


@dataclass
class ActionsParams:
    id: str
    params: dict[str, Union[int, str, Any]] # def = "strolling_npc", x = 11, y = 5

@dataclass
class TriggerType:
    on_enter: str

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
    triggers_type: Optional[Dict[str, TriggerType]] = None
    triggers: Optional[List[TriggerData]] = None


PATH = os.path.abspath('.') + '/assets/'
map_definitions = MapDefinition(
    path=PATH + 'small_room.tmx',
    on_wake=[
        ActionsParams(id='add_npc', params={'def': 'strolling_npc', 'x': 11, 'y': 5}),
        ActionsParams(id='add_npc', params={'def': 'standing_npc', 'x': 2, 'y': 5}),
    ],
    actions={
        'teleport_south': ActionsParams(id='teleport', params={'x': 11, 'y': 3}),
        'teleport_north': ActionsParams(id='teleport', params={'x': 10, 'y': 11}),
    },
    triggers_type={
        'north_door_trigger': { 'on_enter': 'teleport_south' },
        'south_door_trigger': { 'on_enter': 'teleport_north' },
    },
    triggers=[
        TriggerData(trigger='north_door_trigger', x=11, y=2),
        TriggerData(trigger='south_door_trigger', x=10, y=12),
    ]
)