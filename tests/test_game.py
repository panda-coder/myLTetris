"""
Unit tests for the TetrisGame class.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame

# Initialize pygame for testing
pygame.init()
test_surface = pygame.Surface((500, 600))

from tetris.game import TetrisGame
from tetris.constants import MATRIX_WIDTH, MATRIX_HEIGHT, GRID_WIDTH, GRID_HEIGHT, GAME_STATES


class TestTetrisGame(unittest.TestCase):
    """Test cases for the TetrisGame class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.surface = test_surface
        self.game = TetrisGame(self.surface, 20, 60, 360, 490)
    
    def test_game_initialization(self):
        """Test game initialization."""
        self.assertEqual(self.game.surface, self.surface)
        self.assertEqual(self.game.state, GAME_STATES["PLAYING"])
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.lines_cleared, 0)
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsInstance(self.game.blocks, list)
        self.assertEqual(len(self.game.matrix), MATRIX_WIDTH)
        self.assertEqual(len(self.game.matrix[0]), MATRIX_HEIGHT)
    
    def test_matrix_initialization(self):
        """Test matrix initialization."""
        matrix = self.game._initialize_matrix()
        self.assertEqual(len(matrix), MATRIX_WIDTH)
        self.assertEqual(len(matrix[0]), MATRIX_HEIGHT)
        
        # Check all positions are initialized to 0
        for x in range(MATRIX_WIDTH):
            for y in range(MATRIX_HEIGHT):
                self.assertEqual(matrix[x][y], 0)
    
    def test_add_remove_block(self):
        """Test adding and removing blocks."""
        mock_block = Mock()
        
        # Test adding block
        initial_count = len(self.game.blocks)
        self.game.add_block(mock_block)
        self.assertEqual(len(self.game.blocks), initial_count + 1)
        self.assertIn(mock_block, self.game.blocks)
        
        # Test removing block
        self.game.remove_block(mock_block)
        self.assertEqual(len(self.game.blocks), initial_count)
        self.assertNotIn(mock_block, self.game.blocks)
    
    def test_is_position_occupied(self):
        """Test position occupation checking."""
        # Test unoccupied position
        self.assertFalse(self.game.is_position_occupied(5, 5))
        
        # Test occupied position
        self.game.set_matrix_position(5, 5, 1)
        self.assertTrue(self.game.is_position_occupied(5, 5))
        
        # Test negative y (above game area)
        self.assertFalse(self.game.is_position_occupied(5, -1))
        
        # Test out of bounds
        self.assertTrue(self.game.is_position_occupied(-1, 5))
        self.assertTrue(self.game.is_position_occupied(MATRIX_WIDTH, 5))
        self.assertTrue(self.game.is_position_occupied(5, MATRIX_HEIGHT))
    
    def test_set_get_matrix_position(self):
        """Test matrix position setting and getting."""
        # Test valid position
        self.game.set_matrix_position(5, 5, 1)
        self.assertEqual(self.game.get_matrix_value(5, 5), 1)
        
        # Test out of bounds (should not crash)
        self.game.set_matrix_position(-1, 5, 1)
        self.game.set_matrix_position(MATRIX_WIDTH, 5, 1)
        
        # Test negative y
        self.assertEqual(self.game.get_matrix_value(5, -1), 0)
    
    def test_clear_matrix(self):
        """Test matrix clearing."""
        # Set some positions
        self.game.set_matrix_position(5, 5, 1)
        self.game.set_matrix_position(3, 7, 1)
        
        # Clear matrix
        self.game.clear_matrix()
        
        # Check all positions are cleared
        for x in range(MATRIX_WIDTH):
            for y in range(MATRIX_HEIGHT):
                self.assertEqual(self.game.matrix[x][y], 0)
    
    def test_is_line_full(self):
        """Test line fullness checking."""
        y = 10
        
        # Empty line
        self.assertFalse(self.game.is_line_full(y))
        
        # Fill line partially
        for x in range(GRID_WIDTH // 2):
            self.game.set_matrix_position(x, y, 1)
        self.assertFalse(self.game.is_line_full(y))
        
        # Fill line completely
        for x in range(GRID_WIDTH):
            self.game.set_matrix_position(x, y, 1)
        self.assertTrue(self.game.is_line_full(y))
        
        # Test out of bounds
        self.assertFalse(self.game.is_line_full(-1))
        self.assertFalse(self.game.is_line_full(GRID_HEIGHT))
    
    def test_is_game_over(self):
        """Test game over condition."""
        # Game should not be over initially
        self.assertFalse(self.game.is_game_over())
        
        # Place block at top
        self.game.set_matrix_position(5, 0, 1)
        self.assertTrue(self.game.is_game_over())
    
    @patch('tetris.game.Piece')
    def test_spawn_new_piece(self, mock_piece_class):
        """Test spawning new pieces."""
        # Clear current piece
        self.game.current_piece = None
        
        # Spawn new piece
        self.game._spawn_new_piece()
        
        # Check piece was created
        mock_piece_class.assert_called_once()
        self.assertIsNotNone(self.game.current_piece)
    
    def test_handle_input_no_piece(self):
        """Test input handling when no current piece."""
        self.game.current_piece = None
        
        # Should not crash
        self.game.handle_input(pygame.K_DOWN)
        self.game.handle_input(pygame.K_LEFT)
        self.game.handle_input(pygame.K_RIGHT)
    
    def test_handle_input_game_over(self):
        """Test input handling when game is over."""
        self.game.state = GAME_STATES["GAME_OVER"]
        mock_piece = Mock()
        self.game.current_piece = mock_piece
        
        # Input should be ignored
        self.game.handle_input(pygame.K_DOWN)
        mock_piece.move.assert_not_called()
    
    def test_handle_input_valid_moves(self):
        """Test input handling for valid moves."""
        mock_piece = Mock()
        self.game.current_piece = mock_piece
        
        # Test left movement
        self.game.handle_input(pygame.K_LEFT)
        mock_piece.move.assert_called_with("LEFT")
        
        # Test right movement
        mock_piece.reset_mock()
        self.game.handle_input(pygame.K_RIGHT)
        mock_piece.move.assert_called_with("RIGHT")
    
    def test_get_state(self):
        """Test getting game state."""
        self.assertEqual(self.game.get_state(), GAME_STATES["PLAYING"])
        
        self.game.state = GAME_STATES["GAME_OVER"]
        self.assertEqual(self.game.get_state(), GAME_STATES["GAME_OVER"])
    
    def test_get_score_and_lines(self):
        """Test getting score and lines cleared."""
        self.assertEqual(self.game.get_score(), 0)
        self.assertEqual(self.game.get_lines_cleared(), 0)
        
        # Simulate scoring
        self.game.score = 1000
        self.game.lines_cleared = 5
        
        self.assertEqual(self.game.get_score(), 1000)
        self.assertEqual(self.game.get_lines_cleared(), 5)
    
    def test_draw_method_exists(self):
        """Test that draw method exists and can be called."""
        # Should not crash
        self.game.draw()
    
    def test_update_method_exists(self):
        """Test that update method exists and can be called."""
        # Should not crash
        self.game.update()


if __name__ == '__main__':
    unittest.main()