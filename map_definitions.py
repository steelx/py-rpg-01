
from dataclasses import dataclass
from typing import List


@dataclass
class ActionsParams:
    id: str
    params: dict[str, str] # def = "strolling_npc", x = 11, y = 5

@dataclass
class MapDefinition:
    path: str
    on_wake: List[ActionsParams] = None