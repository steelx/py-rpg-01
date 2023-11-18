from entity import Entity
from game import Game
from statemachine import StateMachine
from utils import Animation

ANIM_TIME_MS = 200


class SleepState:
    entity: Entity
    controller: StateMachine
    game: Game

    def __init__(self, character, game: Game):
        from character import Character
        assert isinstance(
            character, Character), "Expected character to be an instance of Character"
        self.character = character
        self.game = game
        self.entity = character.entity
        self.controller = character.controller
        from character_definitions import entities
        self.sleep_entity = Entity(entities["sleeping"], self.game)
        self.anim = Animation(frames=[self.sleep_entity.frame], ms=ANIM_TIME_MS)

    def enter(self, **kwargs):
        self.entity.set_frame(self.character.definition.anim.left[0])
        self.entity.add_child("sleeping", self.sleep_entity)
        self.anim.set_frames((0, 1, 2, 3))

    def exit(self):
        self.entity.remove_child("sleeping")

    def render(self, **kwargs):
        pass

    def update(self, dt: float):
        self.anim.update(dt)
        self.sleep_entity.set_frame(self.anim.frame())

    def change_state(self, dx, dy):
        pass

