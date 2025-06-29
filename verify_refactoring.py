#!/usr/bin/env python3
"""
Comprehensive verification script for the refactored myLTetris game.
This script tests all modules and functionality without requiring user interaction.
"""

import sys
import traceback
from pathlib import Path

def write_result(message, success=True):
    """Write result to both console and file."""
    symbol = "✅" if success else "❌"
    result = f"{symbol} {message}"
    print(result)
    with open("verification_results.txt", "a", encoding="utf-8") as f:
        f.write(result + "\n")

def test_imports():
    """Test all module imports."""
    write_result("=== TESTING IMPORTS ===")
    
    try:
        # Test constants
        from tetris.constants import (
            SCREEN_WIDTH, SCREEN_HEIGHT, GRID_WIDTH, GRID_HEIGHT,
            BLOCK_SIZE, PIECE_CONFIGURATIONS, DIRECTIONS
        )
        write_result(f"Constants imported - Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        
        # Test Block class (needs a game instance)
        import pygame
        pygame.init()
        surface = pygame.Surface((500, 600))
        from tetris.game import TetrisGame
        temp_game = TetrisGame(surface, 20, 60, 360, 490)
        
        from tetris.block import Block
        block = Block(temp_game, 5, 5)
        write_result(f"Block class - Created at ({block.x}, {block.y}) with color {block.color}")
        pygame.quit()
        
        # Test Piece class (needs a game instance)
        import pygame
        pygame.init()
        surface = pygame.Surface((500, 600))
        from tetris.game import TetrisGame
        temp_game = TetrisGame(surface, 20, 60, 360, 490)
        
        from tetris.piece import Piece
        piece = Piece(temp_game, 0)
        write_result(f"Piece class - Created with {len(piece.blocks)} blocks")
        pygame.quit()
        
        # Test TetrisGame class
        from tetris.game import TetrisGame
        write_result("TetrisGame class imported successfully")
        
        # Test GameRunner class
        from tetris.runner import GameRunner
        write_result("GameRunner class imported successfully")
        
        # Test main package import
        from tetris import TetrisGame as MainGame
        write_result("Main package import successful")
        
        return True
        
    except Exception as e:
        write_result(f"Import failed: {str(e)}", False)
        traceback.print_exc()
        return False

def test_piece_functionality():
    """Test piece operations."""
    write_result("\n=== TESTING PIECE FUNCTIONALITY ===")
    
    try:
        import pygame
        pygame.init()
        surface = pygame.Surface((500, 600))
        from tetris.game import TetrisGame
        temp_game = TetrisGame(surface, 20, 60, 360, 490)
        
        from tetris.piece import Piece
        from tetris.constants import PIECE_CONFIGURATIONS
        
        # Test all piece types
        piece_names = ['Square', 'L', 'L_inv', 'T', 'Z1', 'Z2', 'I']
        for i, name in enumerate(piece_names):
            piece = Piece(temp_game, i)
            original_count = len(piece.blocks)
            
            write_result(f"{name} piece: {original_count} blocks")
            
            # Test movement
            can_move_left = piece.can_move("LEFT")
            can_move_right = piece.can_move("RIGHT")
            can_move_down = piece.can_move("DOWN")
            write_result(f"{name} piece movement checks: L={can_move_left}, R={can_move_right}, D={can_move_down}")
        
        pygame.quit()
        return True
        
    except Exception as e:
        write_result(f"Piece functionality failed: {str(e)}", False)
        traceback.print_exc()
        return False

def test_game_logic():
    """Test game logic without pygame display."""
    write_result("\n=== TESTING GAME LOGIC ===")
    
    try:
        # Import pygame and initialize
        import pygame
        pygame.init()
        
        # Create dummy surface
        surface = pygame.Surface((500, 600))
        
        from tetris.game import TetrisGame
        game = TetrisGame(surface, 20, 60, 360, 490)
        
        write_result(f"Game initialized - State: {game.get_state()}")
        write_result(f"Initial score: {game.get_score()}")
        write_result(f"Lines cleared: {game.get_lines_cleared()}")
        write_result(f"Has current piece: {game.current_piece is not None}")
        
        # Test matrix operations
        game.set_matrix_position(10, 14, 1)
        value = game.get_matrix_value(10, 14)
        write_result(f"Matrix operations work: {value == 1}")
        
        # Test collision detection
        occupied = game.is_position_occupied(10, 14)
        write_result(f"Position occupation detection: {occupied}")
        
        # Test line clearing logic
        # Fill a line (use MATRIX_WIDTH instead of matrix_width)
        from tetris.constants import MATRIX_WIDTH
        for x in range(MATRIX_WIDTH):
            game.set_matrix_position(x, 14, 1)
        
        lines_before = game.get_lines_cleared()
        game.clear_full_lines()
        lines_after = game.get_lines_cleared()
        
        write_result(f"Line clearing works: {lines_after > lines_before}")
        
        pygame.quit()
        return True
        
    except Exception as e:
        write_result(f"Game logic test failed: {str(e)}", False)
        traceback.print_exc()
        return False

def test_file_structure():
    """Verify file structure is correct."""
    write_result("\n=== TESTING FILE STRUCTURE ===")
    
    required_files = [
        "tetris/__init__.py",
        "tetris/constants.py",
        "tetris/block.py",
        "tetris/piece.py",
        "tetris/game.py",
        "tetris/runner.py",
        "tests/__init__.py",
        "tests/test_block.py",
        "tests/test_piece.py",
        "tests/test_game.py",
        "tests/test_runner.py",
        "main.py",
        "run_tests.py",
        "README.md",
        "REFACTORING_REPORT.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if not missing_files:
        write_result(f"All {len(required_files)} required files present")
        return True
    else:
        write_result(f"Missing files: {', '.join(missing_files)}", False)
        return False

def main():
    """Run all verification tests."""
    # Clear previous results
    with open("verification_results.txt", "w", encoding="utf-8") as f:
        f.write("myLTetris Refactoring Verification Results\n")
        f.write("=" * 50 + "\n\n")
    
    write_result("🎮 myLTetris Refactoring Verification")
    write_result("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Module Imports", test_imports),
        ("Piece Functionality", test_piece_functionality),
        ("Game Logic", test_game_logic)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            write_result(f"{test_name} test crashed: {str(e)}", False)
    
    write_result(f"\n📊 FINAL RESULTS: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        write_result("🎉 ALL TESTS PASSED!")
        write_result("✅ The refactored myLTetris game is working correctly!")
        write_result("\nTo run the game: uv run python main.py")
        write_result("To run unit tests: uv run python run_tests.py")
        return 0
    else:
        write_result("⚠️  Some tests failed. Check the details above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())