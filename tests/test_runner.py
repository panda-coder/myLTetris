"""
Unit tests for the GameRunner class.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame

from tetris.runner import GameRunner


class TestGameRunner(unittest.TestCase):
    """Test cases for the GameRunner class."""
    
    @patch('tetris.runner.pygame.init')
    @patch('tetris.runner.pygame.display.set_mode')
    @patch('tetris.runner.pygame.time.Clock')
    @patch('tetris.runner.pygame.font.SysFont')
    @patch('tetris.runner.TetrisGame')
    @patch('tetris.runner.pygame.key.set_repeat')
    def test_runner_initialization(self, mock_set_repeat, mock_game_class, 
                                 mock_font, mock_clock, mock_display, mock_init):
        """Test runner initialization."""
        mock_screen = Mock()
        mock_display.return_value = mock_screen
        mock_clock_instance = Mock()
        mock_clock.return_value = mock_clock_instance
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance
        mock_game_instance = Mock()
        mock_game_class.return_value = mock_game_instance
        
        runner = GameRunner()
        
        # Check pygame initialization
        mock_init.assert_called_once()
        mock_display.assert_called_once_with([500, 600])
        mock_screen.fill.assert_called_once()
        
        # Check game initialization
        mock_game_class.assert_called_once()
        
        # Check attributes
        self.assertEqual(runner.screen, mock_screen)
        self.assertEqual(runner.clock, mock_clock_instance)
        self.assertEqual(runner.font, mock_font_instance)
        self.assertEqual(runner.game, mock_game_instance)
        self.assertTrue(runner.running)
        self.assertEqual(runner.fps, 30)
    
    @patch('tetris.runner.pygame.init')
    @patch('tetris.runner.pygame.display.set_mode')
    @patch('tetris.runner.pygame.time.Clock')
    @patch('tetris.runner.pygame.font.SysFont')
    @patch('tetris.runner.TetrisGame')
    @patch('tetris.runner.pygame.key.set_repeat')
    def test_update_display_caption(self, mock_set_repeat, mock_game_class, 
                                   mock_font, mock_clock, mock_display, mock_init):
        """Test display caption updating."""
        # Setup mocks
        mock_screen = Mock()
        mock_display.return_value = mock_screen
        mock_clock_instance = Mock()
        mock_clock_instance.get_fps.return_value = 60.0
        mock_clock_instance.get_rawtime.return_value = 16.7
        mock_clock.return_value = mock_clock_instance
        mock_game_instance = Mock()
        mock_game_instance.get_score.return_value = 1000
        mock_game_instance.get_lines_cleared.return_value = 5
        mock_game_class.return_value = mock_game_instance
        
        with patch('tetris.runner.pygame.display.set_caption') as mock_set_caption:
            runner = GameRunner()
            runner._update_display_caption()
            
            # Check that caption was set
            mock_set_caption.assert_called_once()
            caption = mock_set_caption.call_args[0][0]
            self.assertIn("myLTetris", caption)
            self.assertIn("Score: 1000", caption)
            self.assertIn("Lines: 5", caption)
            self.assertIn("FPS: 60.0", caption)
    
    @patch('tetris.runner.pygame.init')
    @patch('tetris.runner.pygame.display.set_mode')
    @patch('tetris.runner.pygame.time.Clock')
    @patch('tetris.runner.pygame.font.SysFont')
    @patch('tetris.runner.TetrisGame')
    @patch('tetris.runner.pygame.key.set_repeat')
    def test_draw_ui(self, mock_set_repeat, mock_game_class, 
                    mock_font, mock_clock, mock_display, mock_init):
        """Test UI drawing."""
        # Setup mocks
        mock_screen = Mock()
        mock_display.return_value = mock_screen
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = Mock()
        mock_font.return_value = mock_font_instance
        mock_game_instance = Mock()
        mock_game_instance.get_score.return_value = 500
        mock_game_instance.get_lines_cleared.return_value = 3
        mock_game_instance.get_state.return_value = "playing"
        mock_game_class.return_value = mock_game_instance
        
        runner = GameRunner()
        runner._draw_ui()
        
        # Check that screen was filled
        self.assertTrue(mock_screen.fill.called)
        
        # Check that text was rendered and blitted
        self.assertTrue(mock_font_instance.render.called)
        self.assertTrue(mock_screen.blit.called)


if __name__ == '__main__':
    unittest.main()