"""
Game constants and configuration settings.

This module contains all the constants used throughout the game,
making it easy to modify game behavior and maintain consistency.
"""

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

# Game area dimensions
GAME_AREA_X = 20
GAME_AREA_Y = 60
GAME_AREA_WIDTH = 360
GAME_AREA_HEIGHT = 490

# Block dimensions
BLOCK_SIZE = 32
BLOCK_RENDER_SIZE = 30
BLOCK_OFFSET_X = 25
BLOCK_OFFSET_Y = 65

# Game grid dimensions
GRID_WIDTH = 11
GRID_HEIGHT = 15
MATRIX_WIDTH = 30
MATRIX_HEIGHT = 16

# Game settings
DEFAULT_FPS = 30
FONT_SIZE = 35
KEY_REPEAT_DELAY = 200
KEY_REPEAT_INTERVAL = 30

# Colors
BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (255, 255, 255)
MIN_COLOR_VALUE = 100
MAX_COLOR_VALUE = 255

# Piece types
PIECE_TYPES = {
    0: "SQUARE",
    1: "L_SHAPE",
    2: "L_INVERTED",
    3: "T_SHAPE",
    4: "Z_SHAPE_1",
    5: "Z_SHAPE_2",
    6: "I_SHAPE"
}

# Piece configurations (relative positions from center)
PIECE_CONFIGURATIONS = {
    0: [(0, -1), (1, -1), (1, 0), (0, 0)],  # Square
    1: [(0, -2), (0, -1), (0, 0), (1, 0)],   # L
    2: [(0, -2), (0, -1), (0, 0), (-1, 0)],  # L inverted
    3: [(0, -1), (0, 0), (-1, 0), (1, 0)],   # T
    4: [(0, -1), (1, -1), (0, 0), (-1, 0)],  # Z1
    5: [(0, -1), (-1, -1), (0, 0), (1, 0)],  # Z2
    6: [(0, -3), (0, -2), (0, -1), (0, 0)]   # I
}

# Movement directions
DIRECTIONS = {
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
    "DOWN": (0, 1),
    "UP": (0, -1)
}

# Game states
GAME_STATES = {
    "PLAYING": "playing",
    "PAUSED": "paused",
    "GAME_OVER": "game_over"
}