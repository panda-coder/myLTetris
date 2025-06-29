"""
myLTetris - A Python Tetris Game

This package contains the core components of the Tetris game:
- Block: Individual game blocks
- Piece: Tetris pieces composed of blocks
- Game: Main game logic and state management
- Constants: Game configuration and constants
"""

from .game import TetrisGame
from .constants import *

__version__ = "2.0.0"
__author__ = "myLTetris Team"

__all__ = ["TetrisGame"]