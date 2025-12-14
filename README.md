# py-netatmo-truetemp

[![CI](https://github.com/P4uLT/py-netatmo-truetemp/actions/workflows/ci.yml/badge.svg)](https://github.com/P4uLT/py-netatmo-truetemp/actions/workflows/ci.yml)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

A Python client for the Netatmo API with **truetemperature** control - set room temperatures programmatically via the undocumented API endpoint.

## ⚠️ Disclaimer

**Unofficial Project**: This is an independent, community-developed library and is **not affiliated with, endorsed by, or supported by Netatmo or Legrand**.

**Why This Exists**: The official Netatmo OAuth API does not currently support programmatic temperature adjustments via the `truetemperature` endpoint. This library fills that gap using reverse-engineered API endpoints.

**Archival Policy**: This repository will be archived or removed if:
- Netatmo officially adds temperature control support to their OAuth API
- Netatmo requests takedown of this project

**Use at Your Own Risk**: This library relies on undocumented endpoints that may change without notice. Functionality could break if Netatmo modifies their internal API.

## Features

- **TrueTemperature API**: Set room temperatures via Netatmo's undocumented endpoint
- **Room Management**: List and lookup rooms by name (case-insensitive) or ID
- **Smart Updates**: Skips API call if temperature already at target (0.1°C tolerance)
- **Automatic Authentication**: Cookie-based session management with secure storage (0o600)
- **Auto-Retry**: Automatically recovers from authentication failures and API errors
- **Type-Safe**: Full type hints with TypedDict definitions for API responses (Python 3.13+)
- **Thread-Safe**: Safe to use in multi-threaded applications
- **Simple API**: Easy-to-use facade with sensible defaults
- **Extensible**: Modular components for advanced customization
- **Production-Ready**: Comprehensive error handling and logging

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/P4uLT/py-netatmo-truetemp.git
cd py-netatmo-truetemp

# Create virtual environment and install
uv venv
uv sync
```

### As a Dependency

```bash
# Install from GitHub (until PyPI release)
uv add "py-netatmo-truetemp @ git+https://github.com/P4uLT/py-netatmo-truetemp.git"
```

## Environment Variables

Set these required environment variables:

```bash
export NETATMO_USERNAME="your_username"
export NETATMO_PASSWORD="your_password"
```

Optional:
```bash
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

# Get home status
status = api.homestatus(home_id="your-home-id")

# List rooms with thermostats
rooms = api.list_thermostat_rooms()
# Returns: [{'id': '1234567890', 'name': 'Living Room'}, ...]

# Set room temperature (smart update with 0.1°C tolerance)
api.set_truetemperature(
    room_id="1234567890",
    corrected_temperature=20.5
)
```

## Common Use Cases

### Set Temperature by Room Name

```python
from py_netatmo_truetemp import NetatmoAPI
import os

api = NetatmoAPI(
    username=os.environ['NETATMO_USERNAME'],
    password=os.environ['NETATMO_PASSWORD']
)

# Get all rooms
rooms = api.list_thermostat_rooms()
living_room = next(r for r in rooms if r['name'].lower() == 'living room')

# Set temperature
api.set_truetemperature(
    room_id=living_room['id'],
    corrected_temperature=20.5
)
```

### Monitor All Room Temperatures

```python
status = api.homestatus()
for room in status['body']['home']['rooms']:
    temp = room.get('therm_measured_temperature')
    if temp:
        print(f"Room {room['id']}: {temp}°C")
```

### Custom Cookie Location

```python
api = NetatmoAPI(
    username=os.environ['NETATMO_USERNAME'],
    password=os.environ['NETATMO_PASSWORD'],
    cookies_file="/secure/path/cookies.json"
)
```

## How It Works

The library provides a simple `NetatmoAPI` facade that handles all the complexity:

- **Automatic Authentication**: Cookie-based session management with secure storage (0o600 permissions)
- **Smart API Calls**: Auto-retry on authentication failures, skips redundant temperature updates
- **Type-Safe Responses**: Fully typed API responses for better IDE support and error prevention
- **Thread-Safe Operations**: Safe to use in multi-threaded applications with session locking

For advanced usage, you can access individual components directly (see [Advanced Usage](#advanced-usage) below).

For complete architectural details and SOLID design principles, see [CLAUDE.md](CLAUDE.md).

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
   ├── auth_manager.py        # Authentication (thread-safe)
   ├── api_client.py          # HTTP client (auto-retry)
   ├── home_service.py        # Home operations
   ├── thermostat_service.py  # Thermostat operations
   ├── types.py               # TypedDict definitions
   ├── validators.py          # Input validation
   ├── exceptions.py          # Custom exceptions
   ├── constants.py           # API endpoints
   └── logger.py              # Logging utilities

examples/                     # Example applications (independent)
   ├── cli.py                 # CLI entry point
   ├── helpers.py             # Helper functions (API init, error handling)
   ├── display.py             # Display formatting (Rich library)
   ├── pyproject.toml         # Examples dependencies (Typer, Rich)
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

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:

- Code of conduct
- Development setup
- Running tests
- Code style guidelines
- Submitting pull requests

See also:
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [Changelog](CHANGELOG.md)

## Support

- **Bug Reports**: [Open an issue](https://github.com/P4uLT/py-netatmo-truetemp/issues/new?template=bug_report.yml)
- **Feature Requests**: [Request a feature](https://github.com/P4uLT/py-netatmo-truetemp/issues/new?template=feature_request.yml)
- **Security Issues**: See [SECURITY.md](SECURITY.md)
- **Questions**: [GitHub Discussions](https://github.com/P4uLT/py-netatmo-truetemp/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Uses modern Python 3.13+ features and comprehensive type hints
- Built with clean architecture patterns for maintainability (see [CLAUDE.md](CLAUDE.md))
- Inspired by the need for programmatic Netatmo thermostat control
