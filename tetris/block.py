"""
Block module for the Tetris game.

This module contains the Block class which represents individual
blocks that make up Tetris pieces.
"""

import random
from typing import Tuple, TYPE_CHECKING

from .constants import (
    BLOCK_SIZE, BLOCK_RENDER_SIZE, BLOCK_OFFSET_X, BLOCK_OFFSET_Y,
    MIN_COLOR_VALUE, MAX_COLOR_VALUE, GRID_WIDTH, GRID_HEIGHT
)

if TYPE_CHECKING:
    from .game import TetrisGame


class Block:
    """
    Represents a single block in the Tetris game.
    
    Each block has a position, color, and can move within the game grid.
    Blocks are the building components of Tetris pieces.
    """
    
    def __init__(self, game: 'TetrisGame', x: int, y: int):
        """
        Initialize a new block.
        
        Args:
            game: Reference to the main game instance
            x: X coordinate in the game grid
            y: Y coordinate in the game grid
        """
        self.game = game
        self.x = x
        self.y = y
        self.color = self._generate_random_color()
        self.game.add_block(self)
    
    def _generate_random_color(self) -> Tuple[int, int, int]:
        """
        Generate a random RGB color for the block.
        
        Returns:
            Tuple of RGB values
        """
        return (
            random.randint(MIN_COLOR_VALUE, MAX_COLOR_VALUE),
            random.randint(MIN_COLOR_VALUE, MAX_COLOR_VALUE),
            random.randint(MIN_COLOR_VALUE, MAX_COLOR_VALUE)
        )
    
    def can_move_to(self, x: int, y: int) -> bool:
        """
        Check if the block can move to the specified position.
        
        Args:
            x: Target X coordinate
            y: Target Y coordinate
            
        Returns:
            True if the move is valid, False otherwise
        """
        # Check boundaries
        if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
            return False
        
        # Check collision with existing blocks
        if self.game.is_position_occupied(x, y):
            return False
        
        return True
    
    def move_to(self, x: int, y: int) -> bool:
        """
        Move the block to the specified position if possible.
        
        Args:
            x: Target X coordinate
            y: Target Y coordinate
            
        Returns:
            True if the move was successful, False otherwise
        """
        if self.can_move_to(x, y):
            self.x = x
            self.y = y
            return True
        return False
    
    def get_screen_x(self) -> int:
        """Get the X coordinate for rendering on screen."""
        return BLOCK_OFFSET_X + self.x * BLOCK_SIZE
    
    def get_screen_y(self) -> int:
        """Get the Y coordinate for rendering on screen."""
        return BLOCK_OFFSET_Y + self.y * BLOCK_SIZE
    
    def get_render_size(self) -> Tuple[int, int]:
        """Get the size for rendering the block."""
        return (BLOCK_RENDER_SIZE, BLOCK_RENDER_SIZE)
    
    def destroy(self) -> None:
        """Remove this block from the game."""
        self.game.remove_block(self)
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get the block's color."""
        return self.color
    
    def __repr__(self) -> str:
        """String representation of the block."""
        return f"Block(x={self.x}, y={self.y}, color={self.color})"