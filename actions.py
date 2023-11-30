from typing import Dict, Callable

from character import Character
from character_definitions import characters
from game import Game
from ui import Textbox


def teleport(game: Game, tile_x: int, tile_y: int):
    return lambda trigger, entity: entity.set_tile_pos(tile_x, tile_y, game)


def show_textbox(game: Game, tile_x: int, tile_y: int, message: str, chars_per_line: int, lines: int):
    def _show_textbox(trigger, entity):
        pos = game.get_tile_pos_for_ui(tile_x, tile_y)
        game.stack.push(
            Textbox(message, pos=pos, manager=game.manager, chars_per_line=chars_per_line, lines_per_chunk=lines)
        )

    return _show_textbox


def add_npc(game: Game, **params):
    def insert_npc(trigger, entity):
        assert params['def'] in characters, f"Missing 'character name' {params['def']}"
        char_def = characters[params['def']]
        character = Character(char_def, game)
        tile_x = int(params['x']) or character.entity.tile_x
        tile_y = int(params['y']) or character.entity.tile_y
        character.entity.set_tile_pos(tile_x, tile_y, game)
        game.npcs.append(character)

    return insert_npc


ACTIONS: Dict[str, Callable] = {
    "teleport": teleport,
    "add_npc": add_npc,
    "show_textbox": show_textbox,
}
