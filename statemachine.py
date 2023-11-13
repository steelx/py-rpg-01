from state import State


class StateMachine:
    states: dict[str, State]
    current: State | None

    def __init__(self, states: dict[str, State]):
        self.states = states
        self.current = None

    def add(self, state_name, state: State):
        self.states[state_name] = state

    def change(self, state_name, **kwargs):
        if self.current is not None:
            self.current.exit()

        self.current = self.states[state_name]
        self.current.enter(**kwargs)

    def update(self, dt):
        self.current.update(dt)

    def render(self, **kwargs):
        self.current.render(**kwargs)

    def process_event(self, event):
        self.current.process_event(event)
