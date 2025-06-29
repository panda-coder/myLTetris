"""
Unit tests for the Piece class.
"""

import unittest
from unittest.mock import Mock, patch
import pygame

# Initialize pygame for testing
pygame.init()

from tetris.piece import Piece
from tetris.constants import PIECE_CONFIGURATIONS, DIRECTIONS


class TestPiece(unittest.TestCase):
    """Test cases for the Piece class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_game = Mock()
        self.mock_game.add_block = Mock()
        self.mock_game.is_position_occupied_excluding_piece = Mock(return_value=False)
        
    @patch('tetris.piece.Block')
    def test_piece_initialization_with_type(self, mock_block_class):
        """Test piece initialization with specific type."""
        piece = Piece(self.mock_game, 0)  # Square piece
        
        self.assertEqual(piece.piece_type, 0)
        self.assertEqual(piece.game, self.mock_game)
        self.assertFalse(piece.has_collided)
        self.assertEqual(len(piece.blocks), 4)  # Square has 4 blocks
    
    @patch('tetris.piece.Block')
    @patch('tetris.piece.random.randint')
    def test_piece_initialization_random_type(self, mock_randint, mock_block_class):
        """Test piece initialization with random type."""
        mock_randint.return_value = 2
        piece = Piece(self.mock_game, -1)
        
        self.assertEqual(piece.piece_type, 2)
        mock_randint.assert_called_once_with(0, 6)
    
    @patch('tetris.piece.Block')
    def test_create_blocks_square(self, mock_block_class):
        """Test block creation for square piece."""
        piece = Piece(self.mock_game, 0)  # Square piece
        
        # Check that blocks are created with correct positions
        expected_positions = [(5, -1), (6, -1), (6, 0), (5, 0)]
        actual_calls = [call[0] for call in mock_block_class.call_args_list]
        
        for i, (game, x, y) in enumerate(actual_calls):
            self.assertEqual(game, self.mock_game)
            self.assertEqual((x, y), expected_positions[i])
    
    def test_can_move_valid_direction(self):
        """Test movement validation for valid direction."""
        piece = Piece(self.mock_game, 0)
        
        # Mock all blocks to allow movement
        for block in piece.blocks:
            block.x = 5
            block.y = 5
        
        result = piece.can_move("RIGHT")
        self.assertTrue(result)
    
    def test_can_move_invalid_direction(self):
        """Test movement validation for invalid direction."""
        piece = Piece(self.mock_game, 0)
        result = piece.can_move("INVALID")
        self.assertFalse(result)
    
    def test_can_move_blocked_position(self):
        """Test movement validation when position is blocked."""
        piece = Piece(self.mock_game, 0)
        
        # Mock game to return occupied position
        self.mock_game.is_position_occupied_excluding_piece.return_value = True
        
        result = piece.can_move("RIGHT")
        self.assertFalse(result)
    
    def test_move_successful(self):
        """Test successful piece movement."""
        piece = Piece(self.mock_game, 0)
        
        # Store original positions
        original_positions = [(block.x, block.y) for block in piece.blocks]
        
        # Mock movement validation to succeed
        piece.can_move = Mock(return_value=True)
        
        result = piece.move("RIGHT")
        self.assertTrue(result)
        
        # Check that all blocks moved
        dx, dy = DIRECTIONS["RIGHT"]
        for i, block in enumerate(piece.blocks):
            expected_x = original_positions[i][0] + dx
            expected_y = original_positions[i][1] + dy
            self.assertEqual(block.x, expected_x)
            self.assertEqual(block.y, expected_y)
    
    def test_move_failed_down(self):
        """Test failed downward movement sets collision flag."""
        piece = Piece(self.mock_game, 0)
        
        # Mock movement validation to fail
        piece.can_move = Mock(return_value=False)
        
        result = piece.move("DOWN")
        self.assertFalse(result)
        self.assertTrue(piece.has_collided)
    
    def test_move_failed_horizontal(self):
        """Test failed horizontal movement doesn't set collision flag."""
        piece = Piece(self.mock_game, 0)
        
        # Mock movement validation to fail
        piece.can_move = Mock(return_value=False)
        
        result = piece.move("LEFT")
        self.assertFalse(result)
        self.assertFalse(piece.has_collided)
    
    def test_register_blocks(self):
        """Test block registration in game matrix."""
        piece = Piece(self.mock_game, 0)
        self.mock_game.set_matrix_position = Mock()
        
        piece.register_blocks()
        
        # Check that set_matrix_position was called for each block
        self.assertEqual(self.mock_game.set_matrix_position.call_count, len(piece.blocks))
        
        for call in self.mock_game.set_matrix_position.call_args_list:
            args = call[0]
            self.assertEqual(len(args), 3)  # x, y, value
            self.assertEqual(args[2], 1)    # value should be 1
    
    def test_get_block_positions(self):
        """Test getting block positions."""
        piece = Piece(self.mock_game, 0)
        
        positions = piece.get_block_positions()
        self.assertEqual(len(positions), len(piece.blocks))
        
        for i, (x, y) in enumerate(positions):
            self.assertEqual(x, piece.blocks[i].x)
            self.assertEqual(y, piece.blocks[i].y)
    
    def test_is_above_game_area(self):
        """Test checking if piece is above game area."""
        piece = Piece(self.mock_game, 0)
        
        # Set one block above game area
        piece.blocks[0].y = -1
        self.assertTrue(piece.is_above_game_area())
        
        # Set all blocks in game area
        for block in piece.blocks:
            block.y = 5
        self.assertFalse(piece.is_above_game_area())
    
    def test_string_representation(self):
        """Test string representation."""
        piece = Piece(self.mock_game, 0)
        repr_str = repr(piece)
        
        self.assertIn("Piece", repr_str)
        self.assertIn("type=0", repr_str)
        self.assertIn("blocks=4", repr_str)
        self.assertIn("collided=False", repr_str)


if __name__ == '__main__':
    unittest.main()