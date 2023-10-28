from game import Game


class NPCStandState:

    def __init__(self, character, game: Game):
        from character import Character
        assert isinstance(
            character, Character), "Expected character to be an instance of Character"

        self.character = character
        self.game = game
        self.entity = character.entity
        self.controller = character.controller

    def enter(self, **kwargs) -> None:
        pass

    def exit(self) -> None:
        pass

    def render(self, **kwargs) -> None:
        pass

    def update(self, dt: float) -> None:
        pass
