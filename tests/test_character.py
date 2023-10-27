import unittest
from unittest.mock import patch, Mock

import pygame

from character import Character
from character_definitions import characters
from states.wait_state import WaitState


class TestCharacter(unittest.TestCase):

    @patch('pygame.init', return_value=Mock())
    @patch('pygame.display.get_surface', return_value=Mock())
    def setUp(self, mock_get_surface, mock_pygame_init):
        # Mocking pygame's get_surface method to return a Mock object
        # Add any other setup and mocks as needed.
        pass

    @patch('pygame.init', return_value=Mock())
    def test_load_pygame(self, mock_pygame_init):
        pygame.init()
        mock_pygame_init.assert_called_once()

    @patch('states.state_factory.create_state')
    @patch('character_definitions.entities')
    @patch('entity.Entity.create')
    def test_character_initialization(self, mock_entity_create, mock_create_state, mock_entities):
        mock_entities.return_value = {'hero': Mock()}
        mock_create_state.return_value = Mock()
        mock_entity = Mock()
        # Set the 'image' attribute of the mock Entity to another mock that can respond to the 'get_rect()' call
        mock_entity.image.get_rect.return_value = Mock()
        mock_entity_create.return_value = mock_entity

        # self.character_def_data = characters["hero"]
        character_def = characters["hero"]
        game = Mock()

        character = Character(character_def, game)

        # Your assertions to validate the Character class behavior.
        # For instance:
        self.assertEqual(character.facing, character_def.facing)
        self.assertTrue(isinstance(character.controller.current, WaitState))


if __name__ == "__main__":
    unittest.main()
