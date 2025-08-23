#!/usr/bin/env python3
"""
Simple test to verify the refactored modules can be imported and work correctly.
"""


def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        from tetris.constants import SCREEN_HEIGHT, SCREEN_WIDTH

        print(f"✅ Constants imported successfully: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

        from tetris.block import Block

        print("✅ Block class imported successfully")

        from tetris.piece import Piece

        print("✅ Piece class imported successfully")

        from tetris.game import TetrisGame

        print("✅ TetrisGame class imported successfully")

        from tetris.runner import GameRunner

        print("✅ GameRunner class imported successfully")

        from tetris import TetrisGame as MainGame

        print("✅ Main package import successful")

        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality without pygame display."""
    try:
        import pygame

        pygame.init()

        # Create a test surface
        surface = pygame.Surface((500, 600))

        from tetris.game import TetrisGame

        game = TetrisGame(surface, 20, 60, 360, 490)

        print("✅ TetrisGame instance created successfully")
        print(f"   - Initial state: {game.get_state()}")
        print(f"   - Initial score: {game.get_score()}")
        print(f"   - Lines cleared: {game.get_lines_cleared()}")
        print(f"   - Current piece exists: {game.current_piece is not None}")

        # Test matrix operations
        game.set_matrix_position(5, 5, 1)
        value = game.get_matrix_value(5, 5)
        print(f"   - Matrix operations work: set/get value = {value}")

        # Test position checking
        occupied = game.is_position_occupied(5, 5)
        print(f"   - Position occupation check: {occupied}")

        pygame.quit()
        return True

    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False


if __name__ == "__main__":
    print("Testing myLTetris refactored modules...")
    print("=" * 50)

    import_success = test_imports()
    print()

    if import_success:
        functionality_success = test_basic_functionality()
        print()

        if import_success and functionality_success:
            print("🎉 All tests passed! The refactored code is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the error messages above.")
    else:
        print("⚠️  Import tests failed. Cannot proceed with functionality tests.")
