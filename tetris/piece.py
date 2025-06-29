"""
Piece module for the Tetris game.

This module contains the Piece class which represents Tetris pieces
composed of multiple blocks.
"""

import random
from typing import List, TYPE_CHECKING

from .block import Block
from .constants import PIECE_CONFIGURATIONS, DIRECTIONS

if TYPE_CHECKING:
    from .game import TetrisGame


class Piece:
    """
    Represents a Tetris piece composed of multiple blocks.
    
    Each piece has a specific shape and can move and rotate within the game grid.
    """
    
    def __init__(self, game: 'TetrisGame', piece_type: int = -1):
        """
        Initialize a new Tetris piece.
        
        Args:
            game: Reference to the main game instance
            piece_type: Type of piece to create (-1 for random)
        """
        self.game = game
        self.blocks: List[Block] = []
        self.has_collided = False
        
        # Generate random piece type if not specified
        if piece_type == -1:
            piece_type = random.randint(0, len(PIECE_CONFIGURATIONS) - 1)
        
        self.piece_type = piece_type
        self._create_blocks()
    
    def _create_blocks(self) -> None:
        """Create blocks for this piece based on its type."""
        center_x, center_y = 5, 0  # Starting position
        configuration = PIECE_CONFIGURATIONS[self.piece_type]
        
        for dx, dy in configuration:
            block = Block(self.game, center_x + dx, center_y + dy)
            self.blocks.append(block)
    
    def can_move(self, direction: str) -> bool:
        """
        Check if the piece can move in the specified direction.
        
        Args:
            direction: Direction to move ("LEFT", "RIGHT", "DOWN", "UP")
            
        Returns:
            True if the move is valid, False otherwise
        """
        if direction not in DIRECTIONS:
            return False
        
        dx, dy = DIRECTIONS[direction]
        
        # Check if all blocks can move to their new positions
        for block in self.blocks:
            new_x = block.x + dx
            new_y = block.y + dy
            
            # Skip collision check with blocks that are part of this piece
            if not self._can_block_move_to(new_x, new_y):
                return False
        
        return True
    
    def _can_block_move_to(self, x: int, y: int) -> bool:
        """
        Check if a block can move to the specified position,
        ignoring blocks that are part of this piece.
        
        Args:
            x: Target X coordinate
            y: Target Y coordinate
            
        Returns:
            True if the position is valid, False otherwise
        """
        # Check boundaries
        if x < 0 or x >= 11 or y >= 15:  # Using hardcoded values from original
            return False
        
        # Allow movement above the visible area (negative y)
        if y < 0:
            return True
        
        # Check collision with blocks not part of this piece
        if self.game.is_position_occupied_excluding_piece(x, y, self):
            return False
        
        return True
    
    def move(self, direction: str) -> bool:
        """
        Move the piece in the specified direction.
        
        Args:
            direction: Direction to move ("LEFT", "RIGHT", "DOWN", "UP")
            
        Returns:
            True if the move was successful, False otherwise
        """
        if not self.can_move(direction):
            if direction == "DOWN":
                self.has_collided = True
            return False
        
        dx, dy = DIRECTIONS[direction]
        
        # Move all blocks
        for block in self.blocks:
            block.x += dx
            block.y += dy
        
        return True
    
    def register_blocks(self) -> None:
        """Register all blocks of this piece in the game matrix."""
        for block in self.blocks:
            self.game.set_matrix_position(block.x, block.y, 1)
    
    def get_block_positions(self) -> List[tuple]:
        """Get the positions of all blocks in this piece."""
        return [(block.x, block.y) for block in self.blocks]
    
    def is_above_game_area(self) -> bool:
        """Check if any part of the piece is above the visible game area."""
        return any(block.y < 0 for block in self.blocks)
    
    def __repr__(self) -> str:
        """String representation of the piece."""
        return f"Piece(type={self.piece_type}, blocks={len(self.blocks)}, collided={self.has_collided})"