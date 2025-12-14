# Contributing to py-netatmo-truetemp

Thank you for considering contributing to py-netatmo-truetemp! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear descriptive title**
- **Detailed steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Python version** and OS
- **Code sample** demonstrating the issue (if applicable)
- **Error messages** and stack traces

Use the bug report template when creating an issue.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear descriptive title**
- **Detailed description** of the proposed functionality
- **Use cases** explaining why this would be useful
- **Possible implementation** approach (if you have ideas)

### Pull Requests

1. **Fork the repository** and create a branch from `main`
2. **Follow the development setup** below
3. **Make your changes** following code style guidelines
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Run the full test suite** to ensure everything passes
7. **Submit a pull request** with a clear description

## Development Setup

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/py-netatmo-truetemp.git
cd py-netatmo-truetemp

# Create virtual environment and install dependencies
uv venv
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ -v --cov=src/py_netatmo_truetemp --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_netatmo_api.py -v
```

### Code Quality Checks

```bash
# Format code with ruff
uv run ruff format src/ tests/

# Check formatting
uv run ruff format --check src/ tests/

# Run linter
uv run ruff check src/ tests/

# Fix auto-fixable issues
uv run ruff check --fix src/ tests/

# Type checking with mypy
uv run mypy src/py_netatmo_truetemp/

# Security scan with bandit
uv run bandit -r src/py_netatmo_truetemp/ -ll
```

### Running All Checks (CI Simulation)

```bash
# Run the full CI pipeline locally
uv run ruff format --check src/ tests/
uv run ruff check src/ tests/
uv run mypy src/py_netatmo_truetemp/
uv run pytest tests/ -v --cov=src/py_netatmo_truetemp --cov-report=term-missing
uv run bandit -r src/py_netatmo_truetemp/ -ll
```

## Code Style Guidelines

### Python Style

- **Follow PEP 8** conventions (enforced by ruff)
- **Use type hints** for all function signatures and class attributes
- **Write docstrings** for public modules, classes, and functions (Google style)
- **Keep functions focused** and under 50 lines when possible
- **Use descriptive names** (snake_case for functions/variables, PascalCase for classes)

### Type Hints

```python
# Good: Complete type hints with modern syntax
def set_temperature(room_id: str, temperature: float) -> dict[str, Any]:
    """Set room temperature."""
    ...

# Bad: Missing or incomplete type hints
def set_temperature(room_id, temperature):
    ...
```

### Docstrings

```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description of what the function does.

    Longer description providing more context if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param2 is negative
    """
    ...
```

### Architecture Principles

This project follows **SOLID principles** with clean architecture:

1. **Dependency Injection**: All dependencies through constructors
2. **Single Responsibility**: Each class has one reason to change
3. **Open/Closed**: Extend via new classes, not modification
4. **Interface Segregation**: Small, focused interfaces
5. **Dependency Inversion**: Depend on abstractions

Example:
```python
# Good: Dependency injection
class ThermostatService:
    def __init__(self, api_client: NetatmoApiClient, home_service: HomeService):
        self.api_client = api_client
        self.home_service = home_service

# Bad: Creating dependencies internally
class ThermostatService:
    def __init__(self):
        self.api_client = NetatmoApiClient()  # Don't do this!
```

### Testing Guidelines

- **Write tests** for all new functionality
- **Aim for >90% coverage**
- **Use pytest fixtures** for reusable test setup
- **Mock external dependencies** (API calls, file system)
- **Test edge cases** and error conditions

```python
# Good test structure
def test_set_temperature_success(mock_api_client, thermostat_service):
    """Test successful temperature setting."""
    # Arrange
    mock_api_client.post.return_value = {"status": "ok"}

    # Act
    result = thermostat_service.set_room_temperature("123", 20.5)

    # Assert
    assert result["status"] == "ok"
    mock_api_client.post.assert_called_once()
```

## Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat: add new thermostat feature`
- `fix: resolve authentication retry loop`
- `docs: update README installation instructions`
- `test: add coverage for cookie storage`
- `refactor: simplify temperature validation`
- `chore: update dependencies`

## Project Structure

```
src/py_netatmo_truetemp/     # Core library
├── netatmo_api.py           # Main facade
├── api_client.py            # HTTP client
├── auth_manager.py          # Authentication
├── cookie_store.py          # Cookie persistence
├── home_service.py          # Home operations
├── thermostat_service.py    # Thermostat operations
├── types.py                 # TypedDict definitions
├── validators.py            # Input validation
├── exceptions.py            # Custom exceptions
├── constants.py             # API constants
└── logger.py                # Logging utilities

tests/                       # Test suite
├── test_netatmo_api.py
├── test_auth_manager.py
├── test_cookie_store.py
└── ...

examples/                    # Example applications
└── cli.py                   # CLI demonstration
```

## Adding New Features

### Creating a New Service

To add new functionality (e.g., camera support):

1. **Create service class** in `src/py_netatmo_truetemp/camera_service.py`
2. **Inject dependencies** via constructor
3. **Add to NetatmoAPI** facade
4. **Write tests** in `tests/test_camera_service.py`
5. **Update documentation** in README and docstrings
6. **Export from `__init__.py`** if public API

### Extending Existing Features

1. **Check existing code** for patterns to follow
2. **Add functionality** following SOLID principles
3. **Update tests** with new test cases
4. **Update type hints** and docstrings
5. **Run all checks** before submitting PR

## Documentation

- **Update README.md** for user-facing changes
- **Update CLAUDE.md** for architectural changes
- **Update CHANGELOG.md** following Keep a Changelog format
- **Write clear docstrings** for all public APIs
- **Include code examples** for new features

## Release Process

Maintainers follow this process for releases:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with release notes
3. Create git tag: `git tag v0.2.0`
4. Push tag: `git push origin v0.2.0`
5. GitHub Actions automatically publishes to PyPI

## Questions?

- **Check existing issues** for similar questions
- **Open a new issue** with the "question" label
- **Start a discussion** in GitHub Discussions

## Recognition

Contributors will be recognized in:
- Git commit history
- GitHub contributors graph
- Release notes (for significant contributions)

Thank you for contributing to py-netatmo-truetemp!