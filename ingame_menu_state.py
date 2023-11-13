import pygame
import pygame_gui

from state_stack import StateStack
from statemachine import StateMachine
from ui_states import create_state


# stack state
class InGameMenuState:
    should_exit = False

    def __init__(self, display: pygame.Surface, manager: pygame_gui.UIManager, stack: StateStack = None):
        self.stack = stack
        self.manager = manager
        self.display = display

        # create state machine for in game menu
        # controller = ("frontmenu", "items", "magic", "equip", "status")
        controller = ("frontmenu",)
        state_classes = {}  # This will store state classes, not instances.
        for state_name in controller:
            state_class = create_state(state_name)
            assert state_class is not None, f"State {state_name} not found"
            assert state_name not in state_classes, f"State {state_name} already exists"
            state_classes[state_name] = state_class

        self.state_machine = StateMachine({})
        for state_name, state_class in state_classes.items():
            self.state_machine.add(state_name, state_class(self, self.manager, self.display))

    def enter(self) -> None:
        self.state_machine.change("frontmenu")

    def exit(self) -> None:
        pass

    def update(self, dt: float) -> None:
        if self.stack.top() == self:
            self.state_machine.update(dt)

    def render(self) -> None:
        self.state_machine.render()

    def process_event(self, event: pygame.event.Event):
        self.state_machine.process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.should_exit = True
