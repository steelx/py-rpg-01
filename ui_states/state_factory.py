# state factory tries to resolve issues of cyclic imports
from typing import Callable


def create_state(state_name) -> Callable:
    if state_name == "front":
        from .front_menu_state import FrontMenuState
        return FrontMenuState
    if state_name == "item":
        from .item_menu_state import ItemMenuState
        return ItemMenuState
    else:
        raise ValueError(f"Unknown state {state_name}")