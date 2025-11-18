# py-netatmo-truetemp

A Python client for the Netatmo API with **truetemperature** control - set room temperatures programmatically via the undocumented API endpoint.

## Features

- **TrueTemperature API**: Set room temperatures via Netatmo's undocumented endpoint
- **Secure**: JSON-based cookie storage with proper file permissions (0o600)
- **Type-Safe**: Full type hints for better IDE support
- **Modular**: Components can be used independently via dependency injection
- **Extensible**: Easy to add new functionality following SOLID principles
- **Production-Ready**: Comprehensive error handling, auto-retry, and logging

## Installation

```bash
uv venv
uv sync
```

## Environment Variables

Set these required environment variables:

```bash
export NETATMO_USERNAME="your_username"
export NETATMO_PASSWORD="your_password"
```

Optional:
```bash
export NETATMO_SCOPES="read_station read_thermostat write_thermostat..."  # Has sensible defaults
export NETATMO_HOME_ID="your_home_id"  # Auto-detected if not set
```

## Quick Start

```python
import os
from netatmo_api import NetatmoAPI

# Initialize the API (uses cookie-based authentication)
api = NetatmoAPI(
    username=os.environ['NETATMO_USERNAME'],
    password=os.environ['NETATMO_PASSWORD']
)

# Get homes data
homes = api.homesdata()

# Set room temperature
api.set_truetemperature(
    room_id="2631283693",
    corrected_temperature=20.5
)
```

## Task System

The project includes a Taskfile for common operations:

```bash
# Set temperature for Bureau
task bureau TEMP=20.5

# Set temperature for Salle à manger
task salle-a-manger TEMP=21.0

# Set temperature for Chambre Liam
task chambre-liam TEMP=19.3

# List all tasks
task list
```

## Architecture

The codebase uses a layered architecture with dependency injection:

```
NetatmoAPI (Facade)
   ├── CookieStore        - Cookie persistence
   ├── AuthManager        - Authentication flow
   ├── ApiClient          - HTTP communication
   ├── HomeService        - Home operations
   └── ThermostatService  - Thermostat operations
```

## Advanced Usage

For advanced use cases, you can use individual components:

```python
from netatmo_api import (
    CookieStore,
    AuthenticationManager,
    NetatmoApiClient,
    HomeService,
    ThermostatService
)

# Create custom cookie store
cookie_store = CookieStore("/custom/path/cookies.json")

# Inject custom session
import requests
session = requests.Session()
# Configure session as needed...

# Use components directly
auth_manager = AuthenticationManager(
    username="...",
    password="...",
    cookie_store=cookie_store,
    session=session
)
```

## Security

- Credentials should be provided via environment variables
- Session cookies are cached with secure permissions (0o600)
- All API communications use HTTPS
- No unsafe pickle serialization

## Project Structure

```
src/netatmo_api/
   ├── __init__.py              # Package exports
   ├── netatmo_api.py           # Main facade
   ├── cookie_store.py          # Cookie persistence
   ├── auth_manager.py          # Authentication
   ├── api_client.py            # HTTP client
   ├── home_service.py          # Home operations
   ├── thermostat_service.py    # Thermostat operations
   └── logger.py                # Logging utilities
```

## Development

```bash
# Run Python syntax check
python -m py_compile src/netatmo_api/*.py

# Run a task
task bureau TEMP=20.5
```

## Documentation

- [CLAUDE.md](CLAUDE.md) - Development guide for Claude Code

## License

This project demonstrates professional software engineering practices.
