# state factory tries to resolve issues of cyclic imports
from typing import Callable


def create_state(state_name) -> Callable:
    if state_name == "move":
        from move_state import MoveState
        return MoveState
    elif state_name == "wait":
        from wait_state import WaitState
        return WaitState
    else:
        raise ValueError(f"Unknown state {state_name}")
