"""
Game runner module for the Tetris game.

This module contains the main game loop and display management.
"""

import pygame
import random
from typing import Tuple

from .game import TetrisGame
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR,
    GAME_AREA_X, GAME_AREA_Y, GAME_AREA_WIDTH, GAME_AREA_HEIGHT,
    DEFAULT_FPS, FONT_SIZE, KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL,
    GAME_STATES
)


class GameRunner:
    """
    Manages the main game loop, display, and user interface.
    
    This class handles pygame initialization, the main game loop,
    display updates, and user input processing.
    """
    
    def __init__(self):
        """Initialize the game runner."""
        pygame.init()
        
        # Display setup
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.screen.fill(BACKGROUND_COLOR)
        
        # Game setup
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("freesansbold.ttf", FONT_SIZE)
        
        # Initialize game
        self.game = TetrisGame(
            self.screen,
            GAME_AREA_X,
            GAME_AREA_Y,
            GAME_AREA_WIDTH,
            GAME_AREA_HEIGHT
        )
        
        # Input handling
        pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)
        
        # Game state
        self.running = True
        self.fps = DEFAULT_FPS
    
    def _update_display_caption(self) -> None:
        """Update the window caption with game information."""
        fps = self.clock.get_fps()
        raw_time = self.clock.get_rawtime()
        score = self.game.get_score()
        lines = self.game.get_lines_cleared()
        
        caption = (f"myLTetris - Score: {score} | Lines: {lines} | "
                  f"FPS: {fps:.1f} | Frame: {raw_time:.1f}ms | Press ESC to quit")
        pygame.display.set_caption(caption)
    
    def _draw_ui(self) -> None:
        """Draw the user interface elements."""
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        title_color = (0, 0, random.randint(80, 150))
        title_text = self.font.render("myLittleTetris:", True, title_color)
        self.screen.blit(title_text, (20, 10))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.game.get_score()}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 520))
        
        # Draw lines cleared
        lines_text = self.font.render(f"Lines: {self.game.get_lines_cleared()}", True, (255, 255, 255))
        self.screen.blit(lines_text, (20, 550))
        
        # Draw game over message if needed
        if self.game.get_state() == GAME_STATES["GAME_OVER"]:
            game_over_text = self.font.render("GAME OVER!", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
            
            restart_text = pygame.font.SysFont("freesansbold.ttf", 20).render(
                "Press R to restart or ESC to quit", True, (255, 255, 255)
            )
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(restart_text, restart_rect)
    
    def _handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game.get_state() == GAME_STATES["GAME_OVER"]:
                    # Restart game
                    self.game = TetrisGame(
                        self.screen,
                        GAME_AREA_X,
                        GAME_AREA_Y,
                        GAME_AREA_WIDTH,
                        GAME_AREA_HEIGHT
                    )
                else:
                    self.game.handle_input(event.key)
    
    def _update_game(self) -> None:
        """Update game state."""
        self.game.update()
        
        # Auto-move pieces down periodically
        if self.game.get_state() == GAME_STATES["PLAYING"]:
            # Move piece down every second (adjust based on level/difficulty)
            current_time = pygame.time.get_ticks()
            if not hasattr(self, '_last_drop_time'):
                self._last_drop_time = current_time
            
            drop_interval = max(100, 1000 - (self.game.get_lines_cleared() * 50))  # Speed up as lines increase
            
            if current_time - self._last_drop_time > drop_interval:
                self.game.move_current_piece_down()
                self._last_drop_time = current_time
    
    def run(self) -> None:
        """Run the main game loop."""
        while self.running:
            # Control frame rate
            self.clock.tick(self.fps)
            
            # Handle events
            self._handle_events()
            
            # Update game state
            self._update_game()
            
            # Draw everything
            self._draw_ui()
            self.game.draw()
            
            # Update display
            self._update_display_caption()
            pygame.display.update()
        
        # Cleanup
        pygame.quit()


def run_game() -> None:
    """Main entry point for running the game."""
    runner = GameRunner()
    runner.run()