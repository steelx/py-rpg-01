from state import State


class StateMachine:
    states_initiated: dict[str, State]
    states: dict[str, callable]
    current: State | None

    def __init__(self, states: dict[str, callable]):
        self.states = states
        self.current = None
        self.states_initiated = {}

    @staticmethod
    def create(states: dict[str, State]):
        return StateMachine(states)

    def change(self, state_name, **kwargs):
        if self.current is not None:
            self.current.exit()

        if state_name not in self.states_initiated:
            self.states_initiated[state_name] = self.states[state_name]()

        self.current = self.states_initiated[state_name]
        self.current.enter(**kwargs)

    def update(self):
        self.current.update()

    def render(self, **kwargs):
        self.current.render(**kwargs)
