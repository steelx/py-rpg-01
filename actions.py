from typing import Dict, Callable

from game import Game


def teleport(game: Game, tile_x: int, tile_y: int):
    return lambda trigger, entity: entity.teleport(tile_x, tile_y, game)


ACTIONS: Dict[str, Callable] = {
    "teleport": teleport,
}
