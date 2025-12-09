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

## CLI Examples

The `examples/` folder contains demonstration applications showing how to use the library. Each example has its own isolated environment and configuration.

For CLI setup, usage, and development workflow, see **`examples/CLAUDE.md`**.

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
   - `AuthenticationManager`: Authentication flow and token caching
   - `NetatmoApiClient`: HTTP client with automatic retry
   - `HomeService`: Home operations (data, status)
   - `ThermostatService`: Room temperature control
   - `NetatmoAPI`: Facade coordinating all services
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

Uses modern Python 3.10+ syntax:
- `Type | None` (not `Optional[Type]`)
- `dict[K, V]`, `list[T]` (not `Dict`, `List`)
- Return types required for all public methods

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

This project uses a **library + examples** structure for clean separation:

### Core Library (Installable Package)
```
src/py_netatmo_truetemp/    # Installable library package
├── __init__.py             # Public API exports
├── netatmo_api.py          # Facade
├── cookie_store.py         # Cookie persistence
├── auth_manager.py         # Authentication + caching
├── api_client.py           # HTTP + retry
├── home_service.py         # Home operations
├── thermostat_service.py   # Temperature control
├── validators.py           # Input validation
├── exceptions.py           # Custom exceptions
├── constants.py            # API endpoints
└── logger.py               # Logging
```

### Examples (Independent Applications)
```
examples/                   # Independent examples folder
├── cli.py                  # CLI application
├── pyproject.toml          # Examples dependencies
├── .mise.local.toml        # Environment configuration
├── Taskfile.yml            # Task runner configuration
├── .venv/                  # Isolated virtual environment
└── CLAUDE.md               # Examples-specific documentation
```

**Build Configuration**: The root `pyproject.toml` includes `[build-system]` configuration using Hatchling, making the library installable via pip or as an editable dependency.

**Example Applications**: The `examples/` folder contains independent demonstration applications (e.g., CLI tool). Each example has its own environment and uses the library via editable install. See `examples/CLAUDE.md` for setup and usage instructions.

## Development Guidelines

**Code Style**:
- Keep components <250 lines
- One class per file
- Use dependency injection throughout
- snake_case for methods and variables
- PascalCase for classes

**Type Safety**:
- Return types required for all public methods
- Use modern Python 3.10+ type hints (`Type | None`, `dict[K, V]`, `list[T]`)

**Testing**:
- Test library changes using example applications
- Validate with `python -m py_compile src/py_netatmo_truetemp/*.py`

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

# Set room temperature
api.set_truetemperature(room_id="2631283693", temperature=20.5)

# Get home status
status = api.get_home_status(home_id="your-home-id")
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

- **`examples/CLAUDE.md`** - CLI setup, usage, and development workflow
- **`src/py_netatmo_truetemp/__init__.py`** - Public API exports
- **`pyproject.toml`** - Build configuration and dependencies
