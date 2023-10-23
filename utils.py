from typing import Dict, Any, Tuple


def get_faced_tile(character: Dict[str, Any]) -> Tuple[int, int]:
    """
    Get the tile that the character is facing
    :param character: hero["entity"], hero["facing"]
    :return:
    """
    tile_x = character["entity"].tile_x
    tile_y = character["entity"].tile_y
    if character["facing"] == "left":
        tile_x -= 1
    elif character["facing"] == "right":
        tile_x += 1
    elif character["facing"] == "up":
        tile_y -= 1
    elif character["facing"] == "down":
        tile_y += 1
    return tile_x, tile_y
