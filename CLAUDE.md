# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with the core library in this repository.

## Project Overview

This is a reusable Python library for interacting with the Netatmo API, with a focus on thermostat control and temperature management. The library follows SOLID principles with clean architecture patterns.

## Core Library Setup

```bash
# In root directory
uv venv                    # Create virtual environment
uv sync                    # Install dependencies
```

### Validation

```bash
# Syntax check all library modules
python -m py_compile src/py_netatmo_truetemp/*.py
```

## Release Automation

This project uses **semantic-release** for fully automated releases. All versioning, changelog generation, and publishing happens automatically in CI when you push to the main branch.

### Quick Start

```bash
# 1. Make changes with conventional commits
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug"

# 2. Push to main - automatic release happens
git push origin main

# GitHub Actions automatically:
# - Analyzes conventional commits
# - Determines version bump (major/minor/patch)
# - Updates version in pyproject.toml and __init__.py
# - Generates and updates CHANGELOG.md
# - Creates git tag with verified signature
# - Creates GitHub Release
# - Publishes to PyPI
```

That's it! No manual steps required.

### Checking Your Work

Before pushing, verify your commits:

```bash
# View recent commits
git log --oneline -10

# View commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Check if commits follow conventional format
git log --oneline -10 | grep -E "^[a-f0-9]+ (feat|fix|perf|revert|docs|refactor|style|test|chore|ci)"
```

### Conventional Commits

All commits must follow [Conventional Commits](https://www.conventionalcommits.org/) format (enforced by pre-commit hooks):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Common types**:
- `feat:` - New feature (minor version bump: 0.1.0 → 0.2.0)
- `fix:` - Bug fix (patch version bump: 0.1.0 → 0.1.1)
- `feat!:` - Breaking change (major version bump: 0.1.0 → 1.0.0)
- `docs:` - Documentation (no version bump)
- `refactor:` - Code refactoring (no version bump)
- `test:`, `chore:`, `ci:` - Other changes (no version bump)

**Examples**:
```bash
git commit -m "feat: add temperature scheduling"
git commit -m "fix: handle auth timeout errors"
git commit -m "feat!: redesign API interface"
git commit -m "docs: update installation guide"
```

### Configuration Files

**`.releaserc.json`** - semantic-release configuration:
- Defines release rules and commit analysis
- Configures changelog generation with conventional commits
- Specifies version file updates (pyproject.toml, __init__.py)
- Sets commit message format for release commits
- Configures GitHub Release creation

**`.github/workflows/release.yml`** - Automated release workflow:
- Triggers on push to main branch
- Uses semantic-release to analyze commits and determine version
- Updates `pyproject.toml`, `__init__.py`, and `CHANGELOG.md`
- Creates git tags with verified signature (GitHub App)
- Creates GitHub Releases with changelog
- Triggers PyPI publishing workflow

**`.pre-commit-config.yaml`** - Pre-commit hooks:
- Enforces conventional commit message format
- Runs file format checks (trailing whitespace, end-of-file-fixer)
- Validates YAML and TOML syntax

For complete workflow documentation, troubleshooting, and best practices, see **`RELEASE_WORKFLOW_GUIDE.md`**.

### Release Workflow Requirements

**GitHub Ruleset Protection**:
- All changes must go through Pull Requests
- **CI must pass** (`ci-success` status check) before merge
- All commits must be signed (GPG/SSH)
- No direct pushes to main branch
- Merge blocked until all quality gates pass

**If your PR is blocked from merging**:
1. Check CI status in the "Checks" tab of your PR
2. Fix any failing tests, linting issues, or type errors
3. Push fixes to your PR branch
4. CI will automatically re-run
5. Merge button unlocks when all checks pass

**Quality Gates** (all must pass):
- Ruff linting and formatting
- mypy type checking
- pytest tests with coverage (Ubuntu, macOS, Windows)
- Security scan (bandit)
- Package build verification

**Emergency Bypass** (use sparingly):
- Repository admins can bypass ruleset for critical security fixes
- Release bot (GitHub App) can bypass for automated releases
- Document reason in commit message if bypassing

## Architecture Overview

The core library follows **SOLID principles** with a layered architecture using dependency injection throughout.

### Key Architectural Patterns

**Facade Pattern**: `NetatmoAPI` (in `src/py_netatmo_truetemp/netatmo_api.py`) acts as a simple facade coordinating all services. All dependencies flow through constructor injection.

**Layered Architecture**:
```
Application Layer (Consumer applications)
    ↓
Facade Layer (NetatmoAPI)
    ↓
Service Layer (HomeService, ThermostatService)
    ↓
Infrastructure Layer (NetatmoApiClient, AuthenticationManager, CookieStore)
```

### Critical Design Principles

1. **Dependency Injection**: All components receive their dependencies through constructors. Never create dependencies internally (e.g., don't call `requests.Session()` inside a class; inject it instead).

2. **Single Responsibility**: Each component has exactly one reason to change:
   - `CookieStore`: Cookie persistence (JSON with 0o600 permissions)
   - `AuthenticationManager`: Authentication flow and token caching (thread-safe with locking)
   - `NetatmoApiClient`: HTTP client with automatic retry
   - `HomeService`: Home operations (data, status)
   - `ThermostatService`: Room temperature control and room listing
   - `NetatmoAPI`: Facade coordinating all services
   - `types.py`: TypedDict definitions for type-safe API responses
   - `validators.py`: Input validation
   - `exceptions.py`: Custom exceptions
   - `constants.py`: API endpoints and constants

3. **Open/Closed**: To add new functionality (e.g., camera support), create a new service class instead of modifying existing ones.

### Data Flow for Temperature Setting

```
Application → NetatmoAPI.set_truetemperature()
  → ThermostatService.set_room_temperature()
    → HomeService.get_home_status() [fetches current temp]
    → NetatmoApiClient.post("/api/truetemperature")
      → AuthenticationManager.get_auth_headers()
      → requests.Session.post()
```

**Note**: Requires current temperature from `get_home_status()` before setting new temperature (Netatmo API requirement).

### Cookie Storage and Security

Cookies stored as JSON (not pickle) with `0o600` permissions:
- Linux: `~/.cache/netatmo/py-netatmo-truetemp/cookies.json`
- macOS: `~/Library/Caches/netatmo/py-netatmo-truetemp/cookies.json`
- Windows: `%LOCALAPPDATA%\netatmo\py-netatmo-truetemp\Cache\cookies.json`

Customize via `cookies_file` parameter in NetatmoAPI.

### Authentication Flow

Lazy and cached:
1. First API call triggers authentication
2. Loads cached cookies or authenticates fresh
3. Subsequent calls reuse session

### Type Safety

Uses modern Python 3.13+ syntax with comprehensive type definitions:
- `Type | None` (not `Optional[Type]`)
- `dict[K, V]`, `list[T]` (not `Dict`, `List`)
- Return types required for all public methods
- `TypedDict` definitions in `types.py` for all API responses (`HomesDataResponse`, `HomeStatusResponse`, `TrueTemperatureResponse`, etc.)
- Type aliases for common patterns (`ResponseStatus = Literal["ok", "failed"]`)
- Thread-safe session management with locking in `AuthenticationManager`

## Key Features

- **Token Caching**: In-memory + persistent cookies, thread-safe
- **Auto-Retry**: Detects 403 errors, invalidates tokens, retries automatically
- **Smart Updates**: Skips API call if temp already at target (0.1°C tolerance)
- **Validation**: Temperature range (-50°C to 50°C), non-empty IDs
- **Exception Hierarchy**: `NetatmoError`, `AuthenticationError`, `ApiError`, `ValidationError`, `RoomNotFoundError`, `HomeNotFoundError`

## Adding New Features

### Adding a New Service (e.g., Camera Support)

```python
# src/py_netatmo_truetemp/camera_service.py
class CameraService:
    def __init__(self, api_client: NetatmoApiClient):
        self.api_client = api_client

    def get_camera_status(self) -> dict:
        return self.api_client.get("/api/getcamerastatus")
```

Then inject into `NetatmoAPI`:
```python
# In NetatmoAPI.__init__
self.camera_service = CameraService(self.api_client)
```

### Adding Alternative Storage Backend

```python
# Implement same interface as CookieStore
class RedisCookieStore:
    def load(self) -> dict[str, str] | None: ...
    def save(self, cookies: dict[str, str]) -> None: ...
    def clear(self) -> None: ...
```

Inject into `AuthenticationManager` instead of `CookieStore`.

## Debugging

**Authentication issues**: Delete cached cookies (see paths above) and verify credentials
**API failures**: Enable debug logging in `logger.py`, check Netatmo API status
**Temperature not working**: Verify room ID via `homesdata()`, check `get_home_status()` returns valid data
**Import issues**: Ensure `uv sync` completed successfully

## Package Structure

This is a Python library package following modern src-layout structure:

```
src/py_netatmo_truetemp/    # Installable library package
├── __init__.py             # Public API exports
├── netatmo_api.py          # Facade
├── cookie_store.py         # Cookie persistence
├── auth_manager.py         # Authentication + caching
├── api_client.py           # HTTP + retry
├── home_service.py         # Home operations
├── thermostat_service.py   # Temperature control
├── types.py                # TypedDict definitions for API responses
├── validators.py           # Input validation
├── exceptions.py           # Custom exceptions
├── constants.py            # API endpoints
└── logger.py               # Logging
```

**Build Configuration**: The `pyproject.toml` includes `[build-system]` configuration using Hatchling, making the library installable via pip.

**Usage Examples**: For example applications built with this library, see the [py-netatmo-truetemp-cli](https://github.com/P4uLT/py-netatmo-truetemp-cli) repository.

## Development Guidelines

**Code Style**:
- Keep components <250 lines
- One class per file
- Use dependency injection throughout
- snake_case for methods and variables
- PascalCase for classes

**Type Safety**:
- Return types required for all public methods
- Use modern Python 3.13+ type hints (`Type | None`, `dict[K, V]`, `list[T]`)
- TypedDict for structured API responses

**Commit Messages**:
- All commits must follow Conventional Commits format (enforced by pre-commit hooks)
- Use semantic commit types: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `ci:`
- Breaking changes: Use `!` suffix (e.g., `feat!:`) or `BREAKING CHANGE:` footer
- See "Release Automation" section for detailed commit message guidelines

**Testing**:
- Validate with `python -m py_compile src/py_netatmo_truetemp/*.py`
- Run tests: `uv run pytest`

**Pre-commit Hooks**:
- Install hooks: `uv run pre-commit install`
- Hooks automatically validate commit messages, file formatting, and syntax
- Run manually: `uv run pre-commit run --all-files`

## Using the Library

### Basic Usage

```python
from py_netatmo_truetemp import NetatmoAPI

# Initialize with credentials
api = NetatmoAPI(
    username="your.email@example.com",
    password="your-password"
)

# Get homes data
homes = api.homesdata()

# Get home status
status = api.homestatus(home_id="your-home-id")

# List rooms with thermostats
rooms = api.list_thermostat_rooms()
# Returns: [{'id': '1234567890', 'name': 'Living Room'}, ...]

# Set room temperature (supports smart updates with 0.1°C tolerance)
api.set_truetemperature(
    room_id="1234567890",
    corrected_temperature=20.5
)
```

### Advanced Usage

**Custom Cookie Storage**:
```python
api = NetatmoAPI(
    username="...",
    password="...",
    cookies_file="/custom/path/cookies.json"
)
```

**Specifying Home ID**:
```python
api = NetatmoAPI(
    username="...",
    password="...",
    home_id="your-home-id"  # Skip auto-detection
)
```

## See Also

- **`src/py_netatmo_truetemp/__init__.py`** - Public API exports
- **`pyproject.toml`** - Build configuration and dependencies
- **`RELEASE_WORKFLOW_GUIDE.md`** - Complete release automation documentation, troubleshooting, and workflow details
- **`.releaserc.json`** - semantic-release configuration
- **`.github/workflows/release.yml`** - Automated release workflow definition
