import os

from pygame.math import Vector2

ASSETS_PATH = os.path.abspath('.') + '/assets/'
DATA_PATH = os.path.abspath('.') + '/data/'

# screen 16:9 ratio
NATURAL_WIDTH = 720
NATURAL_HEIGHT = 480
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
DISPLAY_SIZE = (NATURAL_WIDTH, NATURAL_HEIGHT)
TILE_SIZE = 16
FPS = 30
