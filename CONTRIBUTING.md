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
7. **Sign your commits** (required by GitHub ruleset)
8. **Submit a pull request** with a clear description

#### Pull Request Requirements

**Your PR cannot merge until all these requirements are met**:

- ✅ All CI checks must pass (`ci-success` status check required)
- ✅ All commits must be signed (GPG/SSH signature required)
- ✅ Commits must follow Conventional Commits format
- ✅ Code must pass linting, type checking, and tests
- ✅ PR must be approved (if required by repository settings)

**If your PR is blocked from merging**:

1. **Check CI Status**: Click the "Checks" tab in your PR to see which checks failed
2. **Review Error Logs**: Click "Details" next to the failed check to see error messages
3. **Fix Issues Locally**: Make changes to fix the failing checks
4. **Commit and Push**: Commit your fixes and push to your PR branch
5. **Wait for CI**: CI will automatically re-run when you push new commits
6. **Merge When Green**: Once all checks pass, the merge button will unlock

**Common CI Failures**:
- Linting errors → Run `uv run ruff check --fix src/ tests/`
- Type errors → Run `uv run mypy src/py_netatmo_truetemp/` and fix issues
- Test failures → Run `uv run pytest tests/ -v` and fix failing tests
- Unsigned commits → Configure commit signing (see below)

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

# Install pre-commit hooks
uv run pre-commit install
```

### Configuring Commit Signing (Required)

All commits must be signed with GPG or SSH. This ensures commit authenticity.

**Option 1: GPG Signing**
```bash
# Generate GPG key (if you don't have one)
gpg --full-generate-key

# List your GPG keys
gpg --list-secret-keys --keyid-format=long

# Configure Git to use GPG signing
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true

# Add GPG key to GitHub
gpg --armor --export YOUR_KEY_ID
# Copy the output and add it to GitHub Settings → SSH and GPG keys
```

**Option 2: SSH Signing (Simpler)**
```bash
# Configure Git to use SSH signing
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true

# Add your SSH public key to GitHub as a signing key
# GitHub Settings → SSH and GPG keys → New SSH key → Key type: Signing Key
```

**Verify signing is working**:
```bash
# Make a test commit
git commit --allow-empty -m "test: verify commit signing"

# Verify the commit is signed
git log --show-signature -1
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

This project **enforces** [Conventional Commits](https://www.conventionalcommits.org/) via pre-commit hook.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Required:** `<type>: <subject>`

**Optional:** `(<scope>)`, `<body>`, `<footer>`

### Commit Types

**Types that affect versioning (semantic versioning):**
- `feat:` → New feature (MINOR version bump: 0.1.0 → 0.2.0)
- `fix:` → Bug fix (PATCH version bump: 0.1.0 → 0.1.1)
- `feat!:` or `BREAKING CHANGE:` → Breaking change (MAJOR version bump: 0.1.0 → 1.0.0)

**Other types (no version bump):**
- `chore:` → Maintenance tasks, dependency updates
- `docs:` → Documentation changes
- `test:` → Test additions or modifications
- `refactor:` → Code restructuring without behavior change
- `style:` → Code formatting, whitespace changes
- `ci:` → CI/CD configuration changes
- `perf:` → Performance improvements
- `build:` → Build system changes

### Examples

```bash
# Simple feature commit
git commit -m "feat: add new thermostat feature"

# Bug fix with scope
git commit -m "fix(auth): resolve authentication retry loop"

# Documentation update
git commit -m "docs: update README installation instructions"

# Breaking change (major version bump)
git commit -m "feat!: remove deprecated cookie_store parameter"

# With detailed body and footer
git commit -m "feat: add room scheduling

Allows users to schedule temperature changes for specific times.
Includes new API endpoints for creating and managing schedules.

Closes #42
Refs #15"
```

### Interactive Commit Helper

If you're unsure about the format, use the interactive commit helper:

```bash
# Guided commit message creation
uv run cz commit

# Or shorter alias
uv run cz c
```

This will prompt you step-by-step to create a properly formatted commit message.

### Pre-commit Enforcement

The pre-commit hook automatically validates commit messages. Invalid commits will be rejected:

```bash
# This will fail
git commit -m "bad commit message"
# Error: Commit message does not follow Conventional Commits format

# This will succeed
git commit -m "feat: add new feature"
```

### Bypassing the Hook (Emergency Only)

In rare cases where you need to bypass validation:

```bash
git commit -m "emergency fix" --no-verify
```

**Warning:** Only use `--no-verify` for emergency hotfixes. All commits should follow conventional format.

### Commit Message Best Practices

1. **Use imperative mood**: "add feature" not "added feature"
2. **Be concise**: Subject line should be ≤ 72 characters
3. **Explain why, not what**: The diff shows what changed; explain why in the body
4. **Reference issues**: Use `Closes #123` or `Refs #456` in footer
5. **Break down changes**: One logical change per commit

### Scope Examples

Scopes are optional but help organize changes:

```bash
feat(api): add new endpoint
fix(auth): resolve token refresh issue
docs(readme): update installation steps
test(thermostat): add integration tests
chore(deps): update dependencies
```

Common scopes in this project:
- `api` - API client changes
- `auth` - Authentication and token management
- `thermostat` - Thermostat service
- `home` - Home service
- `cookie` - Cookie storage
- `cli` - CLI example application
- `deps` - Dependencies
- `ci` - CI/CD workflows

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

**Releases are fully automated** - contributors don't need to manage versions manually!

### How Releases Work

When your PR merges to `main`:

1. **semantic-release** analyzes conventional commit messages
2. If release-worthy (`feat:`, `fix:`, `perf:`), it determines the version bump
3. `CHANGELOG.md` is automatically updated with release notes
4. A git tag is created with verified signature (via GitHub App)
5. GitHub Release is created with changelog
6. Package is automatically published to PyPI

### What Triggers a Release

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` | Minor (0.1.0 → 0.2.0) | New features |
| `fix:` | Patch (0.1.0 → 0.1.1) | Bug fixes |
| `perf:` | Patch (0.1.0 → 0.1.1) | Performance improvements |
| `feat!:` or `BREAKING CHANGE:` | Major (0.1.0 → 1.0.0) | Breaking changes |
| `docs:`, `refactor:`, `test:`, `chore:` | No release | Non-user-facing changes |

### Your Contribution Will Appear In

- `CHANGELOG.md` - Your commit message becomes a changelog entry
- GitHub Releases - Listed in the release notes
- PyPI Package - Included in the published package

**Note**: Only commits that trigger releases appear in CHANGELOG.md. Documentation and refactoring commits don't create releases.

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
