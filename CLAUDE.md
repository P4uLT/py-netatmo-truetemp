# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
uv venv                    # Create virtual environment
uv sync                    # Install dependencies
```

### Running the Application
```bash
# Using task runner (preferred)
task bureau TEMP=20.5              # Set Bureau temperature
task salle-a-manger TEMP=21.0      # Set Salle à manger temperature
task chambre-liam TEMP=19.3        # Set Chambre Liam temperature
task couloir TEMP=18.5             # Set Couloir temperature
task set-temp ROOM_ID=<id> TEMP=20 # Set custom room temperature
task list                          # List all tasks

# Direct CLI usage
uv run python src/netatmo.py --room-id <room_id> --temperature <temp>
uv run python src/netatmo.py --room-id 2631283693 --temperature 20.5
```

### Validation
```bash
python -m py_compile src/netatmo_api/*.py    # Syntax check all modules
python -m py_compile src/netatmo.py          # Syntax check CLI
```

### Required Environment Variables
The application requires these environment variables to be set:
```bash
NETATMO_USERNAME        # Netatmo account username
NETATMO_PASSWORD        # Netatmo account password
```

Optional environment variables:
```bash
NETATMO_SCOPES         # OAuth2 scopes (has sensible defaults)
NETATMO_HOME_ID        # Default home ID (auto-detected if not set)
```

## Architecture Overview

This codebase follows **SOLID principles** with a layered architecture using dependency injection throughout.

### Key Architectural Patterns

**Facade Pattern**: `NetatmoAPI` (in `src/netatmo_api/netatmo_api.py`) acts as a simple facade coordinating all services. All dependencies flow through constructor injection.

**Layered Architecture**:
```
CLI Layer (src/netatmo.py)
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
CLI → NetatmoAPI.set_truetemperature()
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
# src/netatmo_api/camera_service.py
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

**Authentication issues**: Delete cached cookies (see paths above) and check env vars
**API failures**: Enable debug logging in `logger.py`, check Netatmo status
**Temperature not working**: Verify room ID via `homesdata()`, check `get_home_status()` returns valid data

## Code Organization

```
src/
├── netatmo.py              # CLI entry point
└── netatmo_api/
    ├── netatmo_api.py      # Facade
    ├── cookie_store.py     # Cookie persistence
    ├── auth_manager.py     # Authentication + caching
    ├── api_client.py       # HTTP + retry
    ├── home_service.py     # Home operations
    ├── thermostat_service.py # Temperature control
    ├── validators.py       # Input validation
    ├── exceptions.py       # Custom exceptions
    ├── constants.py        # API endpoints
    └── logger.py           # Logging
```

**Guidelines**: Keep components <250 lines, one class per file, use dependency injection, snake_case methods, PascalCase classes
