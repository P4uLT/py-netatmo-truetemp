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
- `pyproject.toml` - CLI dependencies (parent library + Click)
- `.venv/` - Isolated virtual environment
- `.mise.local.toml` - Environment variables and credentials
- `Taskfile.yml` - Pre-configured task shortcuts

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd examples
uv venv        # Creates .venv/ in examples folder
```

### 2. Install Dependencies

```bash
uv sync        # Installs parent library (editable) + Click + dependencies
```

### 3. Configure Environment Variables

Create/edit `.mise.local.toml` with your Netatmo credentials:

```toml
[env]
NETATMO_USERNAME = "your.email@example.com"
NETATMO_PASSWORD = "your-password"
NETATMO_HOME_ID = "your-home-id"  # Optional, auto-detected if omitted

# Optional: Room IDs for task shortcuts
BUREAU_ID = "2631283693"
SALLE_A_MANGER_ID = "123456789"
CHAMBRE_LIAM_ID = "987654321"
COULOIR_ID = "555555555"
```

**Security**: `.mise.local.toml` is git-ignored. Never commit credentials.

## CLI Usage

### Method 1: Task Runner (Recommended)

Pre-configured shortcuts in `Taskfile.yml`:

```bash
# Room-specific shortcuts (requires room IDs in .mise.local.toml)
task bureau TEMP=20.5
task salle-a-manger TEMP=21.0
task chambre-liam TEMP=19.3
task couloir TEMP=18.5

# Generic command for any room
task set-temp ROOM_ID=2631283693 TEMP=20.0

# List all available tasks
task list
```

**Note**: Room shortcuts require environment variables like `BUREAU_ID`, `SALLE_A_MANGER_ID` in `.mise.local.toml`.

### Method 2: Direct CLI Execution

```bash
# List all rooms with thermostats
uv run python cli.py list-rooms

# Set temperature by room ID
uv run python cli.py set-truetemperature --room-id 2631283693 --temperature 20.5

# Set temperature by room name (case-insensitive)
uv run python cli.py set-truetemperature --room-name "Bureau" --temperature 20.5
uv run python cli.py set-truetemperature --room-name "bureau" --temperature 19.0
```

## Development Workflow

### Testing Library Changes

The editable install means library changes are immediately available:

```bash
# 1. Edit library source
vim ../src/py_netatmo_truetemp/thermostat_service.py

# 2. Test immediately (no reinstall needed)
task bureau TEMP=20.5
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
- Click command group definition (`list-rooms`, `set-truetemperature`)
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

### Click Framework

- Type-safe command-line arguments
- Automatic help generation (`--help`)
- Built-in input validation
- Command groups and aliases

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
resolved_id, resolved_name = resolve_room_id(api, None, "Bureau", None)
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

### .mise.local.toml

Environment configuration (git-ignored):
- **Credentials**: `NETATMO_USERNAME`, `NETATMO_PASSWORD`
- **Optional**: `NETATMO_HOME_ID`
- **Room IDs**: `BUREAU_ID`, `SALLE_A_MANGER_ID`, etc. (for task shortcuts)

### Taskfile.yml

Task runner shortcuts:
- Room-specific commands (`task bureau`, `task salle-a-manger`)
- Generic command (`task set-temp`)
- Reads environment variables from `.mise.local.toml`

## Troubleshooting

### CLI-Specific Issues

**Import errors**:
- Ensure `uv sync` completed successfully
- Verify parent library installed: `uv pip list | grep netatmo`

**Authentication failures**:
- Check credentials in `.mise.local.toml`
- Verify environment variables loaded: `env | grep NETATMO`
- Delete cached cookies (see `../CLAUDE.md` for paths)

**Task not found**:
- Verify room ID variables set in `.mise.local.toml`
- Run `task list` to see available tasks

**Library changes not reflected**:
- Editable install works automatically
- If issues persist, try `uv sync` to refresh

**CLI crashes**:
- Check Click version: `uv pip show click`
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
- `click>=8.1.8` - CLI framework
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
