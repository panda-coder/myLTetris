# GitHub Workflows Documentation

This directory contains GitHub Actions workflows for the myLTetris project, providing comprehensive CI/CD automation.

## 🔄 Workflows Overview

### 1. Main CI Pipeline (`ci.yml`)
**Triggers:** Push/PR to main/develop branches

**Features:**
- Multi-Python version testing (3.8-3.12)
- Code quality checks (flake8, black)
- Security scanning (bandit, safety)
- Package building
- Artifact uploads

**Jobs:**
- `test`: Run unit tests across Python versions
- `code-quality`: Security and vulnerability checks
- `build`: Package building and artifact creation

### 2. Comprehensive Testing (`test.yml`)
**Triggers:** Push/PR to main/develop, daily schedule (2 AM UTC)

**Features:**
- Cross-platform testing (Ubuntu, Windows, macOS)
- Multi-Python version matrix (3.8-3.12)
- Test coverage reporting
- Codecov integration
- Pygame headless testing setup

**Special Configurations:**
- Virtual display (Xvfb) for Linux pygame testing
- Platform-specific dependency installation
- Coverage reports with HTML and XML output

### 3. Code Quality (`code-quality.yml`)
**Triggers:** Push/PR to main/develop branches

**Features:**
- Black code formatting checks and auto-formatting
- Import sorting with isort
- Advanced linting with flake8
- Type checking with mypy
- Security analysis with bandit
- Auto-commit formatting fixes on PRs

**Jobs:**
- `lint`: Code quality checks
- `format`: Auto-format code on PRs (if needed)

### 4. Release Automation (`release.yml`)
**Triggers:** GitHub releases, manual workflow dispatch

**Features:**
- Automated PyPI publishing
- Cross-platform executable creation
- Release artifact management
- Dependency on successful tests

**Jobs:**
- `test`: Reuse test workflow
- `build-and-publish`: PyPI package publishing
- `create-executable`: Multi-platform executable creation

## 🛠️ Setup Requirements

### Repository Secrets
For full functionality, configure these secrets in your GitHub repository:

```
PYPI_API_TOKEN    # For PyPI publishing (optional)
CODECOV_TOKEN     # For coverage reporting (optional)
```

### UV Package Manager
This project uses [uv](https://github.com/astral-sh/uv) as the Python package manager. The workflows automatically install and use uv for:
- Dependency management
- Virtual environment handling
- Package building
- Test execution

### Branch Protection
Recommended branch protection rules for `main`:
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Required status checks:
  - `test (ubuntu-latest, 3.11)`
  - `lint`

## 🎮 Pygame Testing Configuration

The workflows include special configuration for testing pygame applications in headless environments:

### Linux (Ubuntu)
```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v3
  with:
    version: "latest"

- name: Install system dependencies
  run: |
    sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
    sudo apt-get install -y xvfb

- name: Install Python dependencies
  run: uv sync

- name: Run tests with virtual display
  run: |
    export DISPLAY=:99
    Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
    uv run python run_tests.py
  env:
    SDL_VIDEODRIVER: dummy
    SDL_AUDIODRIVER: dummy
```

### Windows/macOS
```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v3
  with:
    version: "latest"

- name: Install Python dependencies
  run: uv sync

- name: Run tests
  run: uv run python run_tests.py
  env:
    SDL_VIDEODRIVER: dummy
    SDL_AUDIODRIVER: dummy
```

## 📊 Coverage Reporting

Test coverage is automatically collected and reported:
- **Local HTML reports**: Generated in `htmlcov/` directory
- **XML reports**: For Codecov integration
- **Artifacts**: Coverage reports uploaded as GitHub artifacts
- **Codecov**: Automatic upload for Python 3.11 on Ubuntu

## 🚀 Usage Examples

### Running Tests Locally
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run project test runner
uv run python run_tests.py

# Run with pytest and coverage
uv run pytest tests/ --cov=tetris --cov-report=html -v
```

### Manual Release
```bash
# Trigger release workflow manually
gh workflow run release.yml -f version=1.0.0
```

### Code Quality Checks
```bash
# Format code
uv run black .
uv run isort .

# Lint code
uv run flake8 .

# Security check
uv run bandit -r .
```

## 🔧 Customization

### Adding New Python Versions
Update the matrix in workflow files:
```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11', '3.12', '3.13']
```

### Adding New Operating Systems
Update the matrix in `test.yml`:
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest, ubuntu-20.04]
```

### Modifying Test Commands
Update the test execution steps:
```yaml
- name: Run unit tests
  run: |
    # Your custom test command here
    uv run python -m pytest tests/ -v
```

## 📈 Monitoring

### Workflow Status
- Check workflow runs in the "Actions" tab
- Monitor test results and coverage trends
- Review security scan results

### Artifacts
- Download build artifacts from workflow runs
- Access coverage reports
- Review security scan reports

## 🤝 Contributing

When contributing to this project:
1. Ensure all workflows pass before merging
2. Add tests for new features
3. Update workflow configurations if needed
4. Follow the established code quality standards

The workflows will automatically:
- Run tests on your PRs
- Check code formatting
- Perform security scans
- Generate coverage reports