"""
Unit tests for the Block class.
"""

import unittest
from unittest.mock import Mock, MagicMock
import pygame

# Initialize pygame for testing
pygame.init()

from tetris.block import Block
from tetris.constants import BLOCK_OFFSET_X, BLOCK_OFFSET_Y, BLOCK_SIZE, BLOCK_RENDER_SIZE


class TestBlock(unittest.TestCase):
    """Test cases for the Block class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_game = Mock()
        self.mock_game.add_block = Mock()
        self.mock_game.is_position_occupied = Mock(return_value=False)
        self.block = Block(self.mock_game, 5, 3)
    
    def test_block_initialization(self):
        """Test block initialization."""
        self.assertEqual(self.block.x, 5)
        self.assertEqual(self.block.y, 3)
        self.assertEqual(self.block.game, self.mock_game)
        self.assertIsInstance(self.block.color, tuple)
        self.assertEqual(len(self.block.color), 3)
        self.mock_game.add_block.assert_called_once_with(self.block)
    
    def test_color_generation(self):
        """Test random color generation."""
        color = self.block._generate_random_color()
        self.assertIsInstance(color, tuple)
        self.assertEqual(len(color), 3)
        for component in color:
            self.assertGreaterEqual(component, 100)
            self.assertLessEqual(component, 255)
    
    def test_can_move_to_valid_position(self):
        """Test movement to valid position."""
        self.mock_game.is_position_occupied.return_value = False
        self.assertTrue(self.block.can_move_to(6, 4))
    
    def test_can_move_to_occupied_position(self):
        """Test movement to occupied position."""
        self.mock_game.is_position_occupied.return_value = True
        self.assertFalse(self.block.can_move_to(6, 4))
    
    def test_can_move_to_boundary_positions(self):
        """Test movement to boundary positions."""
        # Left boundary
        self.assertFalse(self.block.can_move_to(-1, 4))
        # Right boundary
        self.assertFalse(self.block.can_move_to(11, 4))
        # Bottom boundary
        self.assertFalse(self.block.can_move_to(5, 15))
    
    def test_move_to_valid_position(self):
        """Test successful movement."""
        self.mock_game.is_position_occupied.return_value = False
        result = self.block.move_to(6, 4)
        self.assertTrue(result)
        self.assertEqual(self.block.x, 6)
        self.assertEqual(self.block.y, 4)
    
    def test_move_to_invalid_position(self):
        """Test failed movement."""
        self.mock_game.is_position_occupied.return_value = True
        original_x, original_y = self.block.x, self.block.y
        result = self.block.move_to(6, 4)
        self.assertFalse(result)
        self.assertEqual(self.block.x, original_x)
        self.assertEqual(self.block.y, original_y)
    
    def test_screen_coordinates(self):
        """Test screen coordinate calculations."""
        expected_x = BLOCK_OFFSET_X + self.block.x * BLOCK_SIZE
        expected_y = BLOCK_OFFSET_Y + self.block.y * BLOCK_SIZE
        self.assertEqual(self.block.get_screen_x(), expected_x)
        self.assertEqual(self.block.get_screen_y(), expected_y)
    
    def test_render_size(self):
        """Test render size."""
        size = self.block.get_render_size()
        self.assertEqual(size, (BLOCK_RENDER_SIZE, BLOCK_RENDER_SIZE))
    
    def test_destroy(self):
        """Test block destruction."""
        self.mock_game.remove_block = Mock()
        self.block.destroy()
        self.mock_game.remove_block.assert_called_once_with(self.block)
    
    def test_get_color(self):
        """Test color getter."""
        color = self.block.get_color()
        self.assertEqual(color, self.block.color)
    
    def test_string_representation(self):
        """Test string representation."""
        repr_str = repr(self.block)
        self.assertIn("Block", repr_str)
        self.assertIn(str(self.block.x), repr_str)
        self.assertIn(str(self.block.y), repr_str)


if __name__ == '__main__':
    unittest.main()