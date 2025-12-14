# CLAUDE.md - CLI Examples

This file provides guidance for working with the CLI examples in this folder.

## Overview

This `examples/` folder contains an **independent CLI application** demonstrating how to use the `py-netatmo-truetemp` library. It has its own virtual environment, dependencies, and configuration separate from the parent library.

For core library architecture, design patterns, and API documentation, see **`../CLAUDE.md`**.

## Key Concepts

### Editable Install

The CLI depends on the parent library using an **editable install**:

```toml
[tool.uv.sources]
py-netatmo-truetemp = { path = "..", editable = true }
```

**Development workflow**:
1. Edit library code in `../src/py_netatmo_truetemp/`
2. Run CLI immediately - changes are live
3. No reinstallation needed

### Independent Environment

This folder has its own isolated setup:
- `pyproject.toml` - CLI dependencies (parent library + Typer)
- `.venv/` - Isolated virtual environment

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd examples
uv venv        # Creates .venv/ in examples folder
```

### 2. Install Dependencies

```bash
uv sync        # Installs parent library (editable) + Typer + dependencies
```

### 3. Configure Environment Variables

Set your Netatmo credentials as environment variables:

```bash
export NETATMO_USERNAME="your.email@example.com"
export NETATMO_PASSWORD="your-password"
export NETATMO_HOME_ID="your-home-id"  # Optional, auto-detected if omitted
```

**Security**: Never commit credentials to version control.

## CLI Usage

```bash
# List all rooms with thermostats
uv run python cli.py list-rooms

# Set temperature by room ID
uv run python cli.py set-truetemperature --room-id 1234567890 --temperature 20.5

# Set temperature by room name (case-insensitive)
uv run python cli.py set-truetemperature --room-name "Living Room" --temperature 20.5
uv run python cli.py set-truetemperature --room-name "living room" --temperature 19.0
```

## Development Workflow

### Testing Library Changes

The editable install means library changes are immediately available:

```bash
# 1. Edit library source
vim ../src/py_netatmo_truetemp/thermostat_service.py

# 2. Test immediately (no reinstall needed)
uv run python cli.py set-truetemperature --room-name "Living Room" --temperature 20.5
```

### Validation

```bash
# Syntax check all CLI modules
python -m py_compile cli.py helpers.py display.py

# Syntax check library
python -m py_compile ../src/py_netatmo_truetemp/*.py
```

### Adding New CLI Examples

Create new Python files demonstrating library usage:

```python
# examples/monitor.py
from py_netatmo_truetemp import NetatmoAPI
import os

api = NetatmoAPI(
    username=os.environ["NETATMO_USERNAME"],
    password=os.environ["NETATMO_PASSWORD"]
)

homes = api.homesdata()
print(f"Found {len(homes)} homes")
```

Run with:
```bash
uv run python monitor.py
```

## CLI Architecture

The CLI demonstrates best practices for using the library with a clean, modular architecture:

### Module Organization

**`cli.py`** - Application entry point:
- Typer app definition (`list-rooms`, `set-truetemperature`)
- Command routing and parameter handling
- Delegates to helper and display modules

**`helpers.py`** - Business logic and API operations:
- `NetatmoConfig.from_environment()` - Loads credentials from environment
- `create_netatmo_api_with_spinner()` - Initializes API with loading indicator
- `handle_api_errors()` - Decorator for consistent error handling across commands
- `resolve_room_id()` - Resolves room name to ID (supports case-insensitive lookup)
- `validate_room_input()` - Validates mutual exclusivity of room-id/room-name

**`display.py`** - Presentation layer (Rich library):
- `display_rooms_table()` - Formatted table with room list
- `display_temperature_result()` - Success message for temperature changes
- `display_error_panel()` - Styled error panels with red borders

### Typer Framework

- Type-safe command-line arguments with Annotated pattern
- Automatic help generation (`--help`)
- Built-in input validation
- Modern Python 3.13+ type hints support
- Rich integration for beautiful terminal output

### Library Integration Pattern

```python
# Modular pattern from helpers.py and cli.py
from py_netatmo_truetemp import NetatmoAPI
import os

# Initialize with environment variables (via helper)
api = create_netatmo_api_with_spinner()

# List rooms with thermostats
rooms = api.list_thermostat_rooms()

# Set temperature by room name (dynamic lookup)
resolved_id, resolved_name = resolve_room_id(api, None, "Living Room", None)
api.set_truetemperature(
    room_id=resolved_id,
    corrected_temperature=20.5
)
```

### Error Handling

- Decorator-based error handling (`@handle_api_errors`)
- Catches all library exceptions (`NetatmoError`, `AuthenticationError`, `ValidationError`, etc.)
- Rich-formatted error panels with descriptive messages
- Exits with appropriate status codes (via `click.Abort()`)

## Configuration Files

### pyproject.toml

Defines CLI dependencies:
```toml
[project]
name = "netatmo-cli-examples"
dependencies = [
    "py-netatmo-truetemp",  # Parent library (editable)
    "click>=8.1.8",         # CLI framework
    "rich>=14.2.0",         # Terminal formatting (tables, panels, colors)
]

[tool.uv.sources]
py-netatmo-truetemp = { path = "..", editable = true }
```

### Environment Variables

Required environment variables:
- **Credentials**: `NETATMO_USERNAME`, `NETATMO_PASSWORD`
- **Optional**: `NETATMO_HOME_ID`

## Troubleshooting

### CLI-Specific Issues

**Import errors**:
- Ensure `uv sync` completed successfully
- Verify parent library installed: `uv pip list | grep netatmo`

**Authentication failures**:
- Check environment variables are set: `env | grep NETATMO`
- Verify credentials are correct
- Delete cached cookies (see `../CLAUDE.md` for paths)

**Library changes not reflected**:
- Editable install works automatically
- If issues persist, try `uv sync` to refresh

**CLI crashes**:
- Check Typer version: `uv pip show typer`
- Enable debug logging in library (see `../CLAUDE.md`)

### Getting Help

For library-level issues (authentication, API errors, architecture questions), see **`../CLAUDE.md`**.

## Adding CLI Dependencies

```bash
# Add new dependency to examples
uv add <package-name>

# Example: Add another formatting library
uv add tabulate
```

**Note**: Parent library dependencies (requests, platformdirs) are automatically available. The CLI already includes:
- `typer[all]>=0.9.0` - CLI framework with Rich integration
- `rich>=14.2.0` - Terminal formatting (tables, panels, spinners)

## Best Practices

1. **Keep examples simple** - Focus on demonstrating library usage
2. **Never hardcode credentials** - Always use environment variables
3. **Handle errors gracefully** - Catch library exceptions and provide user-friendly messages
4. **Test with real devices** - Ensure examples work with actual Netatmo hardware
5. **Document new examples** - Add usage instructions and explanations

## See Also

- **`../CLAUDE.md`** - Core library architecture, design patterns, and API documentation
- **`../src/py_netatmo_truetemp/`** - Library source code
- **`cli.py`** - CLI implementation demonstrating library usage
