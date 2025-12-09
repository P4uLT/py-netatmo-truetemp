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
1. Edit library code in `../src/netatmo_api/`
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
uv run python cli.py --room-id <room_id> --temperature <temp>

# Examples
uv run python cli.py --room-id 2631283693 --temperature 20.5
uv run python cli.py --room-id 2631283693 --temperature 19.0
```

## Development Workflow

### Testing Library Changes

The editable install means library changes are immediately available:

```bash
# 1. Edit library source
vim ../src/netatmo_api/thermostat_service.py

# 2. Test immediately (no reinstall needed)
task bureau TEMP=20.5
```

### Validation

```bash
# Syntax check CLI
python -m py_compile cli.py

# Syntax check library
python -m py_compile ../src/netatmo_api/*.py
```

### Adding New CLI Examples

Create new Python files demonstrating library usage:

```python
# examples/monitor.py
from netatmo_api import NetatmoAPI
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

The CLI demonstrates best practices for using the library:

### Click Framework

- Type-safe command-line arguments
- Automatic help generation (`--help`)
- Built-in input validation

### Library Integration Pattern

```python
# cli.py shows simple library usage
from netatmo_api import NetatmoAPI
import os

# Initialize with environment variables
api = NetatmoAPI(
    username=os.environ["NETATMO_USERNAME"],
    password=os.environ["NETATMO_PASSWORD"]
)

# Single method call for operations
api.set_truetemperature(room_id=room_id, temperature=temperature)
```

### Error Handling

- Catches library exceptions (`NetatmoError`, `AuthenticationError`, etc.)
- Provides user-friendly error messages
- Exits with appropriate status codes

## Configuration Files

### pyproject.toml

Defines CLI dependencies:
```toml
[project]
name = "netatmo-cli-examples"
dependencies = [
    "py-netatmo-truetemp",  # Parent library (editable)
    "click>=8.1.8",         # CLI framework
]

[tool.uv.sources]
py-netatmo-truetemp = { path = "..", editable = true }
```

### .mise.local.toml

Environment configuration (git-ignored):
- **Credentials**: `NETATMO_USERNAME`, `NETATMO_PASSWORD`
- **Optional**: `NETATMO_HOME_ID`, `NETATMO_SCOPES`
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

# Example: Add tabulate for formatted output
uv add tabulate
```

**Note**: Parent library dependencies (requests, platformdirs) are automatically available.

## Best Practices

1. **Keep examples simple** - Focus on demonstrating library usage
2. **Never hardcode credentials** - Always use environment variables
3. **Handle errors gracefully** - Catch library exceptions and provide user-friendly messages
4. **Test with real devices** - Ensure examples work with actual Netatmo hardware
5. **Document new examples** - Add usage instructions and explanations

## See Also

- **`../CLAUDE.md`** - Core library architecture, design patterns, and API documentation
- **`../src/netatmo_api/`** - Library source code
- **`cli.py`** - CLI implementation demonstrating library usage
