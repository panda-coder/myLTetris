#!/usr/bin/env python3
"""
myLTetris - A Python Tetris Game

This is the main entry point for the refactored Tetris game.
The game has been completely restructured with improved code organization,
better documentation, and enhanced maintainability.

Features:
- Modular code structure
- Comprehensive documentation
- Improved error handling
- Better game state management
- Enhanced user interface

Usage:
    python main.py

Controls:
    - Arrow Keys: Move pieces
    - ESC: Quit game
    - R: Restart game (when game over)
    - D: Debug matrix (development)
"""

from tetris.runner import run_game


def main():
    """Main entry point for the Tetris game."""
    try:
        run_game()
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Thanks for playing!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your pygame installation and try again.")


if __name__ == "__main__":
    main()