# myLTetris

A classic Tetris game implementation in Python using Pygame.

## Description

myLTetris is a simple yet functional Tetris clone featuring:
- Classic Tetris gameplay mechanics
- 7 different tetromino pieces (Square, L-shapes, T-shape, Z-shapes, and I-piece)
- Line clearing when rows are filled
- Collision detection
- Real-time FPS display
- Colorful randomly-generated block colors

## Features

- **Classic Tetris Pieces**: All standard tetromino shapes including:
  - Square (O-piece)
  - L-piece and reverse L-piece
  - T-piece
  - Z-piece and S-piece  
  - I-piece (straight line)

- **Game Mechanics**:
  - Automatic piece falling
  - Manual piece movement (left, right, down)
  - Line clearing when rows are completely filled
  - Game over detection when pieces reach the top
  - Collision detection for piece placement

- **Visual Features**:
  - Colorful blocks with random RGB colors
  - Real-time FPS counter in window title
  - Clean game board with white border

## Requirements

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Pygame

## Installation

### Using uv (Recommended)

1. Install uv if you haven't already:
```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

2. Clone this repository:
```bash
git clone <repository-url>
cd myLTetris
```

3. Install dependencies:
```bash
uv sync
```

### Using pip (Alternative)

1. Clone this repository:
```bash
git clone <repository-url>
cd myLTetris
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

### Using uv (Recommended)

1. Run the game directly:
```bash
uv run python myLTetris.py
```

2. Or use the script entry point:
```bash
uv run myLTetris
```

3. Or use the Makefile:
```bash
make run
```

### Using pip

1. Run the game:
```bash
python myLTetris.py
```

2. **Controls**:
   - **Left Arrow**: Move piece left
   - **Right Arrow**: Move piece right  
   - **Down Arrow**: Move piece down faster
   - **D Key**: Debug - print game matrix to console
   - **Escape**: Quit game

3. **Objective**:
   - Arrange falling pieces to create complete horizontal lines
   - Complete lines will be cleared automatically
   - Game ends when pieces reach the top of the playing field

## Game Window

- **Window Size**: 500x600 pixels
- **Playing Field**: 11x15 grid
- **Title**: Displays "myLitteTetris" with FPS information

## Code Structure

The game is organized into three main classes:

- **`Bloco`**: Represents individual blocks that make up tetromino pieces
- **`Peca`**: Represents complete tetromino pieces with movement logic
- **`Telinha`**: Main game screen class handling game state, rendering, and logic

## Technical Details

- Built with Pygame for graphics and input handling
- Uses a matrix-based collision detection system
- Implements automatic piece generation with random selection
- Features a game loop running at 30 FPS by default

## Development

The game is written in Portuguese variable names and comments, reflecting its original development context. The core game logic follows standard Tetris mechanics with some custom implementations for piece movement and line clearing.

### Development Setup

1. Install development dependencies:
```bash
uv sync --dev
```

2. Available development commands:
```bash
# Format code
make format
# or
uv run black myLTetris.py

# Lint code
make lint
# or
uv run flake8 myLTetris.py

# Run tests (when available)
make test
# or
uv run pytest

# Clean cache files
make clean
```

### Project Structure

- `myLTetris.py` - Main game file with all classes and game logic
- `pyproject.toml` - Project configuration and dependencies
- `requirements.txt` - Legacy pip requirements (kept for compatibility)
- `.python-version` - Specifies Python version for uv
- `Makefile` - Common development tasks

### Package Management with uv

This project uses [uv](https://docs.astral.sh/uv/) for fast and reliable Python package management. Benefits include:

- **Fast**: Much faster than pip for dependency resolution and installation
- **Reliable**: Deterministic dependency resolution with lock files
- **Compatible**: Works with existing pip/PyPI ecosystem
- **Modern**: Built-in support for pyproject.toml and modern Python packaging standards

Key uv commands for this project:
- `uv sync` - Install dependencies
- `uv sync --dev` - Install with development dependencies
- `uv run <command>` - Run commands in the project environment
- `uv add <package>` - Add new dependencies
- `uv remove <package>` - Remove dependencies

## License

This project is open source. Feel free to modify and distribute as needed.

---

*Enjoy playing myLTetris!*
