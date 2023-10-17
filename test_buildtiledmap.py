import unittest

from buildtiledmap import point_to_tile


class TestBuildTiledMap(unittest.TestCase):
    def test_point_to_tile(self):
        self.assertEqual(
            point_to_tile(16, 16, 16, 320, 240),
            (1, 1)
        )
