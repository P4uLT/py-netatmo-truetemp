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
from py_netatmo_truetemp import NetatmoAPI

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
from py_netatmo_truetemp import (
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

This project uses a **library + examples** structure:

```
src/py_netatmo_truetemp/     # Core library (installable package)
   ├── __init__.py            # Package exports
   ├── netatmo_api.py         # Main facade
   ├── cookie_store.py        # Cookie persistence
   ├── auth_manager.py        # Authentication
   ├── api_client.py          # HTTP client
   ├── home_service.py        # Home operations
   ├── thermostat_service.py  # Thermostat operations
   ├── validators.py          # Input validation
   ├── exceptions.py          # Custom exceptions
   ├── constants.py           # API endpoints
   └── logger.py              # Logging utilities

examples/                     # Example applications (independent)
   ├── cli.py                 # CLI application
   ├── pyproject.toml         # Examples dependencies
   ├── Taskfile.yml           # Task runner configuration
   ├── .venv/                 # Isolated virtual environment
   └── README.md              # CLI setup and usage
```

## Development

### Library Development

```bash
# Syntax check library modules
python -m py_compile src/py_netatmo_truetemp/*.py
```

### Testing with Examples

The `examples/` folder contains independent applications for testing library changes. See [`examples/README.md`](examples/README.md) for setup and usage instructions.

## Documentation

- [CLAUDE.md](CLAUDE.md) - Core library architecture and development guide
- [examples/README.md](examples/README.md) - CLI setup and usage instructions
- [examples/CLAUDE.md](examples/CLAUDE.md) - CLI development workflow

## License

This project demonstrates professional software engineering practices.
