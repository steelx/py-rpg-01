from storyboard import Storyboard, Event, Wait


def remove_state(id_: str):
    def create_event(storyboard: Storyboard) -> Event:
        storyboard.remove_state(id_)
        return Wait(0)

    return create_event
