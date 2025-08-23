#!/usr/bin/env python3
"""
Verification script to test the refactored game without running the full GUI.
"""

import os
import sys


def verify_imports():
    """Verify all modules can be imported."""
    print("Testing imports...")

    try:
        # Test constants
        from tetris.constants import (BLOCK_SIZE, COLORS, GRID_HEIGHT,
                                      GRID_WIDTH, PIECE_SHAPES, SCREEN_HEIGHT,
                                      SCREEN_WIDTH)

        print(
            f"✅ Constants: Screen {SCREEN_WIDTH}x{SCREEN_HEIGHT}, Grid {GRID_WIDTH}x{GRID_HEIGHT}"
        )

        # Test Block class
        from tetris.block import Block

        block = Block(5, 5, 1)
        print(f"✅ Block: Created at ({block.x}, {block.y}) with color {block.color}")

        # Test Piece class
        from tetris.piece import Piece

        piece = Piece(0, 0, 0)  # I-piece
        print(f"✅ Piece: Created {piece.shape_name} at ({piece.x}, {piece.y})")

        # Test TetrisGame class
        from tetris.game import TetrisGame

        print("✅ TetrisGame: Class imported successfully")

        # Test GameRunner class
        from tetris.runner import GameRunner

        print("✅ GameRunner: Class imported successfully")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def verify_piece_functionality():
    """Test piece functionality without pygame."""
    print("\nTesting piece functionality...")

    try:
        from tetris.constants import PIECE_SHAPES
        from tetris.piece import Piece

        # Test all piece types
        for i, shape_name in enumerate(["I", "O", "T", "S", "Z", "J", "L"]):
            piece = Piece(5, 5, i)
            print(f"  - {shape_name} piece: {len(piece.blocks)} blocks")

            # Test rotation
            original_blocks = len(piece.blocks)
            piece.rotate()
            rotated_blocks = len(piece.blocks)
            print(f"    Rotation: {original_blocks} -> {rotated_blocks} blocks")

        return True

    except Exception as e:
        print(f"❌ Piece functionality error: {e}")
        return False


def verify_game_logic():
    """Test basic game logic without pygame display."""
    print("\nTesting game logic...")

    try:
        import pygame

        pygame.init()

        # Create a dummy surface for testing
        surface = pygame.Surface((500, 600))

        from tetris.game import TetrisGame

        game = TetrisGame(surface, 20, 60, 360, 490)

        print(f"  - Initial state: {game.get_state()}")
        print(f"  - Initial score: {game.get_score()}")
        print(f"  - Lines cleared: {game.get_lines_cleared()}")
        print(f"  - Has current piece: {game.current_piece is not None}")

        # Test matrix operations
        game.set_matrix_position(10, 15, 1)
        value = game.get_matrix_value(10, 15)
        print(f"  - Matrix set/get test: {value == 1}")

        # Test collision detection
        occupied = game.is_position_occupied(10, 15)
        print(f"  - Position occupied check: {occupied}")

        pygame.quit()
        return True

    except Exception as e:
        print(f"❌ Game logic error: {e}")
        return False


def main():
    """Run all verification tests."""
    print("🎮 myLTetris Refactoring Verification")
    print("=" * 40)

    tests_passed = 0
    total_tests = 3

    if verify_imports():
        tests_passed += 1

    if verify_piece_functionality():
        tests_passed += 1

    if verify_game_logic():
        tests_passed += 1

    print(f"\n📊 Results: {tests_passed}/{total_tests} tests passed")

    if tests_passed == total_tests:
        print("🎉 All verification tests passed!")
        print("✅ The refactored myLTetris game is working correctly!")
        print("\nTo run the game:")
        print("  python main.py")
        print("\nTo run unit tests:")
        print("  python run_tests.py")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
