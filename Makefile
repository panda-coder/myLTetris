.PHONY: install run dev test clean format lint

# Install dependencies using uv
install:
	uv sync

# Run the game
run:
	uv run python myLTetris.py

# Run the game using the script entry point
run-script:
	uv run myLTetris

# Install development dependencies
dev:
	uv sync --dev

# Run tests
test:
	uv run pytest

# Format code
format:
	uv run black myLTetris.py

# Lint code
lint:
	uv run flake8 myLTetris.py

# Clean up cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Show help
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies using uv"
	@echo "  run         - Run the game directly"
	@echo "  run-script  - Run the game using script entry point"
	@echo "  dev         - Install development dependencies"
	@echo "  test        - Run tests"
	@echo "  format      - Format code with black"
	@echo "  lint        - Lint code with flake8"
	@echo "  clean       - Clean up cache files"