# py-netatmo-truetemp

[![CI](https://github.com/P4uLT/py-netatmo-truetemp/actions/workflows/ci.yml/badge.svg)](https://github.com/P4uLT/py-netatmo-truetemp/actions/workflows/ci.yml)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

A Python client for the Netatmo API with **truetemperature** control - set room temperatures programmatically via the undocumented API endpoint.

## Features

- **TrueTemperature API**: Set room temperatures via Netatmo's undocumented endpoint
- **Room Management**: List and lookup rooms by name (case-insensitive) or ID
- **Smart Updates**: Skips API call if temperature already at target (0.1°C tolerance)
- **Secure**: JSON-based cookie storage with proper file permissions (0o600)
- **Type-Safe**: Full type hints with TypedDict definitions for API responses (Python 3.13+)
- **Thread-Safe**: Thread-safe authentication with session locking
- **Modular**: Components can be used independently via dependency injection
- **Extensible**: Easy to add new functionality following SOLID principles
- **Production-Ready**: Comprehensive error handling, auto-retry, and logging

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

## Architecture

The codebase uses a layered architecture with dependency injection following SOLID principles:

```
NetatmoAPI (Facade)
   ├── CookieStore        - Cookie persistence (JSON, 0o600 permissions)
   ├── AuthManager        - Authentication flow (thread-safe with locking)
   ├── ApiClient          - HTTP communication (auto-retry on 403)
   ├── HomeService        - Home operations (homesdata, homestatus)
   └── ThermostatService  - Thermostat operations (list rooms, set temperature)
```

**Key Design Principles:**
- **Dependency Injection**: All components receive dependencies via constructors
- **Single Responsibility**: Each component has one reason to change
- **Type Safety**: TypedDict definitions for all API responses (see `types.py`)
- **Thread Safety**: Session management protected with locks

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
   ├── pyproject.toml         # Examples dependencies (Click, Rich)
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

- Built with clean architecture principles and SOLID design
- Uses modern Python 3.13+ features and type hints
- Inspired by the need for programmatic thermostat control
