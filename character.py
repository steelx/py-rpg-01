from character_definitions import CharacterDefData, entities
from entity import Entity
from game import Game
from statemachine import StateMachine
from states.state_factory import create_state


class Character:
    def __init__(self, character_def: CharacterDefData, game: Game):
        self.game = game
        self.definition = character_def
        entity_def = entities.get(character_def.entity)
        assert entity_def is not None, f"Entity definition {character_def.entity} not found"
        self.entity = Entity(entity_def, game)
        self.anim = character_def.anim
        self.facing = character_def.facing
        self.default_state = character_def.state

        state_classes = {}  # This will store state classes, not instances.
        for state_name in character_def.controller:
            state_class = create_state(state_name)
            assert state_class is not None, f"State {state_name} not found"
            assert state_name not in state_classes, f"State {state_name} already exists"
            state_classes[state_name] = state_class

        self.controller = StateMachine({})

        # Now that self.controller is initialized, create instances of states
        for state_name, state_class in state_classes.items():
            self.controller.add(state_name, state_class(self, game))

        self.controller.change(character_def.state)
