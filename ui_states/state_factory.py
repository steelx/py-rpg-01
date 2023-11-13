# state factory tries to resolve issues of cyclic imports
from typing import Callable


def create_state(state_name) -> Callable:
    if state_name == "frontmenu":
        from .frontmenu_state import FrontMenuState
        return FrontMenuState
    else:
        raise ValueError(f"Unknown state {state_name}")