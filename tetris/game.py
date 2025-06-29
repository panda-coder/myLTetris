"""
Main game logic for the Tetris game.

This module contains the TetrisGame class which manages the game state,
handles user input, and coordinates all game components.
"""

import pygame
import random
from typing import List, Optional, Tuple, TYPE_CHECKING

from .constants import (
    GRID_WIDTH, GRID_HEIGHT, MATRIX_WIDTH, MATRIX_HEIGHT,
    BACKGROUND_COLOR, BORDER_COLOR, GAME_STATES
)

if TYPE_CHECKING:
    from .block import Block
    from .piece import Piece


class TetrisGame:
    """
    Main game class that manages the Tetris game state and logic.
    
    This class handles the game matrix, piece management, line clearing,
    collision detection, and game state management.
    """
    
    def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int):
        """
        Initialize the Tetris game.
        
        Args:
            surface: Pygame surface to draw on
            x: X position of the game area
            y: Y position of the game area
            width: Width of the game area
            height: Height of the game area
        """
        self.surface = surface
        self.game_area = pygame.Rect(x, y, width, height)
        
        # Game state
        self.state = GAME_STATES["PLAYING"]
        self.blocks: List['Block'] = []
        self.current_piece: Optional['Piece'] = None
        self.next_piece_type = random.randint(0, 6)
        self.score = 0
        self.lines_cleared = 0
        
        # Game matrix for collision detection
        self.matrix = self._initialize_matrix()
        
        # Create first piece
        self._spawn_new_piece()
    
    def _initialize_matrix(self) -> List[List[int]]:
        """
        Initialize the game matrix for collision detection.
        
        Returns:
            2D list representing the game grid
        """
        matrix = []
        for _ in range(MATRIX_WIDTH):
            column = [0] * MATRIX_HEIGHT
            matrix.append(column)
        return matrix
    
    def _spawn_new_piece(self) -> None:
        """Spawn a new piece at the top of the game area."""
        from .piece import Piece  # Import here to avoid circular imports
        
        piece_type = self.next_piece_type
        self.next_piece_type = random.randint(0, 6)
        self.current_piece = Piece(self, piece_type)
    
    def add_block(self, block: 'Block') -> None:
        """Add a block to the game."""
        self.blocks.append(block)
    
    def remove_block(self, block: 'Block') -> None:
        """Remove a block from the game."""
        if block in self.blocks:
            self.blocks.remove(block)
    
    def is_position_occupied(self, x: int, y: int) -> bool:
        """
        Check if a position is occupied in the game matrix.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if position is occupied, False otherwise
        """
        if y < 0:
            return False
        if x < 0 or x >= MATRIX_WIDTH or y >= MATRIX_HEIGHT:
            return True
        return self.matrix[x][y] == 1
    
    def is_position_occupied_excluding_piece(self, x: int, y: int, piece: 'Piece') -> bool:
        """
        Check if a position is occupied, excluding blocks from a specific piece.
        
        Args:
            x: X coordinate
            y: Y coordinate
            piece: Piece to exclude from collision check
            
        Returns:
            True if position is occupied, False otherwise
        """
        if y < 0:
            return False
        if x < 0 or x >= MATRIX_WIDTH or y >= MATRIX_HEIGHT:
            return True
        
        # Check if any non-piece block occupies this position
        for block in self.blocks:
            if block not in piece.blocks and block.x == x and block.y == y:
                return True
        
        return False
    
    def set_matrix_position(self, x: int, y: int, value: int) -> None:
        """Set a position in the game matrix."""
        if 0 <= x < MATRIX_WIDTH and 0 <= y < MATRIX_HEIGHT:
            self.matrix[x][y] = value
    
    def get_matrix_value(self, x: int, y: int) -> int:
        """Get the value at a position in the game matrix."""
        if y < 0:
            return 0
        if x < 0 or x >= MATRIX_WIDTH or y >= MATRIX_HEIGHT:
            return 1
        return self.matrix[x][y]
    
    def clear_matrix(self) -> None:
        """Clear the entire game matrix."""
        for x in range(MATRIX_WIDTH):
            for y in range(MATRIX_HEIGHT):
                self.matrix[x][y] = 0
    
    def update_matrix(self) -> None:
        """Update the matrix with current block positions."""
        self.clear_matrix()
        for block in self.blocks:
            if block not in (self.current_piece.blocks if self.current_piece else []):
                if 0 <= block.x < MATRIX_WIDTH and 0 <= block.y < MATRIX_HEIGHT:
                    self.matrix[block.x][block.y] = 1
    
    def is_line_full(self, y: int) -> bool:
        """Check if a horizontal line is completely filled."""
        if y < 0 or y >= GRID_HEIGHT:
            return False
        
        for x in range(GRID_WIDTH):
            if self.matrix[x][y] == 0:
                return False
        return True
    
    def clear_line(self, y: int) -> None:
        """Clear a specific line and move blocks above it down."""
        # Remove blocks on this line
        blocks_to_remove = [block for block in self.blocks 
                           if block.y == y and block not in (self.current_piece.blocks if self.current_piece else [])]
        
        for block in blocks_to_remove:
            block.destroy()
        
        # Move blocks above this line down
        for block in self.blocks:
            if (block not in (self.current_piece.blocks if self.current_piece else []) and 
                block.y < y):
                block.y += 1
        
        self.lines_cleared += 1
        self.score += 100 * self.lines_cleared  # Bonus for multiple lines
    
    def clear_full_lines(self) -> int:
        """Clear all full lines and return the number of lines cleared."""
        lines_cleared_this_turn = 0
        
        # Check from bottom to top
        for y in range(GRID_HEIGHT - 1, -1, -1):
            if self.is_line_full(y):
                self.clear_line(y)
                lines_cleared_this_turn += 1
                # Check the same line again since blocks moved down
                y += 1
        
        return lines_cleared_this_turn
    
    def is_game_over(self) -> bool:
        """Check if the game is over (blocks reached the top)."""
        for x in range(GRID_WIDTH):
            if self.matrix[x][0] == 1:
                return True
        return False
    
    def move_current_piece_down(self) -> bool:
        """
        Move the current piece down one step.
        
        Returns:
            True if the piece moved successfully, False if it collided
        """
        if not self.current_piece:
            return False
        
        success = self.current_piece.move("DOWN")
        
        if self.current_piece.has_collided:
            # Piece has landed, register its blocks and spawn new piece
            self.current_piece.register_blocks()
            self.update_matrix()
            self.clear_full_lines()
            
            if self.is_game_over():
                self.state = GAME_STATES["GAME_OVER"]
                return False
            
            self._spawn_new_piece()
        
        return success
    
    def handle_input(self, key: int) -> None:
        """
        Handle keyboard input.
        
        Args:
            key: Pygame key constant
        """
        if not self.current_piece or self.state != GAME_STATES["PLAYING"]:
            return
        
        if key == pygame.K_DOWN:
            self.move_current_piece_down()
        elif key == pygame.K_LEFT:
            self.current_piece.move("LEFT")
        elif key == pygame.K_RIGHT:
            self.current_piece.move("RIGHT")
        elif key == pygame.K_d:
            # Debug: print matrix
            self._debug_print_matrix()
    
    def _debug_print_matrix(self) -> None:
        """Print the current game matrix for debugging."""
        print("Game Matrix:")
        for y in range(min(10, MATRIX_HEIGHT)):  # Print first 10 rows
            row = ""
            for x in range(GRID_WIDTH):
                row += str(self.matrix[x][y])
            print(f"Row {y}: {row}")
    
    def draw(self) -> None:
        """Draw the game area and all blocks."""
        # Draw game area border
        pygame.draw.rect(self.surface, BORDER_COLOR, self.game_area, 1)
        
        # Draw all visible blocks
        for block in self.blocks:
            if block.y >= 0:  # Only draw blocks in visible area
                screen_x = block.get_screen_x()
                screen_y = block.get_screen_y()
                size = block.get_render_size()
                
                pygame.draw.rect(
                    self.surface,
                    block.get_color(),
                    (screen_x, screen_y, size[0], size[1]),
                    0
                )
    
    def update(self) -> None:
        """Update game state."""
        if self.state == GAME_STATES["PLAYING"]:
            self.update_matrix()
    
    def get_state(self) -> str:
        """Get the current game state."""
        return self.state
    
    def get_score(self) -> int:
        """Get the current score."""
        return self.score
    
    def get_lines_cleared(self) -> int:
        """Get the number of lines cleared."""
        return self.lines_cleared