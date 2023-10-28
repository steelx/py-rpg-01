import os
import unittest

import pygame

from game import Game
from map_definitions import MapDefinition

PATH = os.path.abspath('.') + '/assets/'


class TestMapBuilder(unittest.TestCase):
    """
    The tests might not run in environments without a display, like some CI/CD systems.
    @patch('pygame.display.get_surface', return_value=Mock())
    @patch('pygame.display.init', return_value=None)
    @patch('pygame.display.set_mode', return_value=Mock())
    def setUp(self, mock_get_surface, mock_display_init, mock_set_mode):
        # Mocking pygame's get_surface and display init methods to return a Mock object
        # Add any other setup and mocks as needed.
        pass
    """

    def setUp(self):
        pygame.init()
        pygame.display.set_caption("jRPG Game")
        pygame.display.set_mode((320, 240))

    def test_point_to_tile(self):
        test_map = Game()
        test_map.setup(MapDefinition(path=PATH + 'small_room.tmx'), None)
        self.assertEqual(
            test_map.point_to_tile(16, 16),
            (1, 1)
        )


if __name__ == "__main__":
    unittest.main()
