import os

from pygame.math import Vector2

ASSETS_PATH = os.path.abspath('.') + '/assets/'
DATA_PATH = os.path.abspath('.') + '/data/'

# screen 16:9 ratio
NATURAL_WIDTH = 320
NATURAL_HEIGHT = 180
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
DISPLAY_SIZE = (NATURAL_WIDTH, NATURAL_HEIGHT)
TILE_SIZE = 16
FPS = 30

# overlay positions
OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'seed': (70, SCREEN_HEIGHT - 5)}

PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50, 40),
    'right': Vector2(50, 40),
    'up': Vector2(0, -10),
    'down': Vector2(0, 50)
}

LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'main': 7,
    'house top': 8,
    'fruit': 9,
    'rain drops': 10
}
