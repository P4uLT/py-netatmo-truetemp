# py-netatmo-truetemp

[![PyPI version](https://badge.fury.io/py/py-netatmo-truetemp.svg)](https://pypi.org/project/py-netatmo-truetemp/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/py-netatmo-truetemp)](https://pypi.org/project/py-netatmo-truetemp/)
[![CI](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/actions/workflows/ci.yml/badge.svg)](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/actions/workflows/ci.yml)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/py-netatmo-unofficial/py-netatmo-truetemp/graph/badge.svg)](https://codecov.io/gh/py-netatmo-unofficial/py-netatmo-truetemp)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

**Netatmo's missing true temperature API** - set real room temps programmatically via the undocumented truetemperature endpoint.

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

### From PyPI

```bash
pip install py-netatmo-truetemp
```

Or with uv:
```bash
uv add py-netatmo-truetemp
```

### From Source

```bash
# Clone the repository
git clone https://github.com/py-netatmo-unofficial/py-netatmo-truetemp.git
cd py-netatmo-truetemp

# Create virtual environment and install
uv venv
uv sync
```

### As a Dependency

**From PyPI** (recommended):
```bash
uv add py-netatmo-truetemp
```

**From GitHub** (development version):
```bash
uv add "py-netatmo-truetemp @ git+https://github.com/py-netatmo-unofficial/py-netatmo-truetemp.git"
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

## Usage Examples

### Command-Line Interface

For a complete CLI application built with this library, see:
- **[py-netatmo-truetemp-cli](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp-cli)** - Full-featured CLI with Typer and Rich formatting

The CLI demonstrates:
- Environment-based configuration
- Error handling patterns
- Room lookup by name
- Formatted terminal output

### More Examples

Want to add your project here? Submit a PR or open an issue!

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

## Development

### Library Development

```bash
# Syntax check library modules
python -m py_compile src/py_netatmo_truetemp/*.py
```

### Release Automation

This project uses **semantic-release** for fully automated releases. All versioning, changelog generation, and publishing happens automatically in CI when you push to the main branch.

**Quick workflow:**
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

All commits must follow [Conventional Commits](https://www.conventionalcommits.org/) format:
- `feat:` - New features (minor version bump: 0.1.0 → 0.2.0)
- `fix:` - Bug fixes (patch version bump: 0.1.0 → 0.1.1)
- `feat!:` or `BREAKING CHANGE:` - Breaking changes (major version bump: 0.1.0 → 1.0.0)

Pre-commit hooks enforce commit message validation. For complete release workflow documentation, see [RELEASE_WORKFLOW_GUIDE.md](RELEASE_WORKFLOW_GUIDE.md).

## Documentation

- [CLAUDE.md](CLAUDE.md) - Core library architecture and development guide
- [RELEASE_WORKFLOW_GUIDE.md](RELEASE_WORKFLOW_GUIDE.md) - Release automation and workflow guide

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:

- Code of conduct
- Development setup
- Running tests
- Code style guidelines
- Conventional commit message format (required)
- Submitting pull requests

All commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) format. Pre-commit hooks will validate your commit messages automatically.

See also:
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [Changelog](CHANGELOG.md)
- [Release Workflow Guide](RELEASE_WORKFLOW_GUIDE.md)

## Support

- **Bug Reports**: [Open an issue](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/new?template=bug_report.yml)
- **Feature Requests**: [Request a feature](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/new?template=feature_request.yml)
- **Security Issues**: See [SECURITY.md](SECURITY.md)
- **Questions**: [GitHub Discussions](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Uses modern Python 3.13+ features and comprehensive type hints
- Built with clean architecture patterns for maintainability (see [CLAUDE.md](CLAUDE.md))
- Inspired by the need for programmatic Netatmo thermostat control
