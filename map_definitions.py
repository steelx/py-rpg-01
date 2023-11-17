import os
from dataclasses import dataclass, field, fields
from typing import List, Union, Any, Optional, Dict


@dataclass
class ActionsParams:
    id: str
    params: dict[str, Union[int, str, Any]]  # def = "strolling_npc", x = 11, y = 5


@dataclass
class TriggerDef:
    on_enter: Optional[str] = field(default=None, repr=False)
    on_exit: Optional[str] = field(default=None, repr=False)
    on_use: Optional[str] = field(default=None, repr=False)


class Trigger:
    @staticmethod
    def empty_function(*args, **kwargs):
        """Default empty function."""
        pass

    def __init__(self, definition: TriggerDef = TriggerDef()):
        self.on_enter = definition.on_enter or self.empty_function
        self.on_exit = definition.on_exit or self.empty_function
        self.on_use = definition.on_use or self.empty_function


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
    triggers_type: Optional[Dict[str, TriggerDef]] = None
    triggers_at_tile: Optional[List[TriggerData]] = None


PATH = os.path.abspath('.') + '/assets/'
small_room_map_def = MapDefinition(
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
        'north_door_trigger': TriggerDef(on_enter='teleport_south'),
        'south_door_trigger': TriggerDef(on_enter='teleport_north'),
        'snake': TriggerDef(on_use='teleport_inside_true'),
    },
    triggers_at_tile=[
        TriggerData(trigger='north_door_trigger', x=11, y=3),
        TriggerData(trigger='south_door_trigger', x=10, y=12),
        TriggerData(trigger='snake', x=11, y=6),
    ]
)

player_house_map_def = MapDefinition(
    path=PATH + 'maps/player_house.tmx',
    on_wake=[
        ActionsParams(id='add_npc', params={'def': 'standing_npc', 'x': 27, 'y': 17}),
    ]
)


def create_map_triggers(map_def: MapDefinition, actions, game) -> Dict[str, Trigger]:
    # Create the Trigger types from the map_def
    triggers: Dict[str, Trigger] = {}

    if map_def.triggers_at_tile is None:
        return triggers

    def set_trigger_action(key: str, action_type: str, action_params):
        if action_params:
            triggers[key].__setattr__(
                action_type, actions[action_params.id](game, **action_params.params)
            )

    for trigger_data in map_def.triggers_at_tile:
        trigger_type_id = trigger_data.trigger
        x, y = trigger_data.x, trigger_data.y
        key = f"{x},{y}"
        triggers[key] = Trigger()
        trigger_type = map_def.triggers_type.get(trigger_type_id)

        for trigger_key in fields(trigger_type):
            action_type = trigger_key.name
            action_name = getattr(trigger_type, action_type)
            action_params = map_def.actions.get(action_name)
            set_trigger_action(key, action_type, action_params)

    return triggers
