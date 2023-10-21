from state import State


class StateMachine:
    states: dict[str, callable]
    current: State | None

    def __init__(self, states: dict[str, callable]):
        self.states = states
        self.current = None

    @staticmethod
    def create(states: dict[str, State]):
        return StateMachine(states)

    def change(self, state_name, **kwargs):
        if self.current is not None:
            self.current.exit()
        self.current = self.states[state_name]()
        # print(f"Changing state to {state_name} with kwargs {kwargs}")
        self.current.enter(**kwargs)

    def update(self):
        self.current.update()

    def render(self, **kwargs):
        self.current.render(**kwargs)
