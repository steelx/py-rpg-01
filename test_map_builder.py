import unittest

from map_builder import MapBuilder


class TestMapBuilder(unittest.TestCase):
    def test_point_to_tile(self):
        # TODO: mock pygame init
        test_map = MapBuilder('assets/cave/cave_map.tmx')
        self.assertEqual(
            test_map.point_to_tile(16, 16),
            (1, 1)
        )
