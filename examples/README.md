# Netatmo CLI Example

Example CLI application demonstrating how to use the `py-netatmo-truetemp` library with a clean, modular architecture.

## Features

- **List Rooms**: Display all rooms with thermostats in a formatted table
- **Set Temperature**: Change room temperature by room ID or name (case-insensitive)
- **Rich Formatting**: Beautiful terminal output with tables, panels, and spinners
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Task Runner**: Pre-configured shortcuts for common operations

## Setup

### 1. Create Virtual Environment

```bash
cd examples
uv venv
```

### 2. Install Dependencies

This will install the parent package as an editable dependency along with CLI dependencies (Typer, Rich):

```bash
uv sync
```

### 3. Configure Environment

Set your Netatmo credentials as environment variables:

```bash
export NETATMO_USERNAME="your.email@example.com"
export NETATMO_PASSWORD="your-password"
export NETATMO_HOME_ID="your-home-id"  # Optional, auto-detected if omitted
```

## Usage

### Task Runner (Recommended)

The example includes a Taskfile for convenient shortcuts:

**Development tasks:**
```bash
task install           # Install all dependencies
task lint              # Run ruff linter
task format            # Format code with ruff
task test              # Run tests
task clean             # Clean cache files
```

**CLI shortcuts:**
```bash
task list-rooms        # List all rooms (alias: task ls, task rooms)
task set-temp ROOM="Living Room" TEMP=20.5   # Set temperature with prompt
```

### Direct CLI Usage

**List all rooms with thermostats:**
```bash
uv run python cli.py list-rooms
```

**Set temperature by room ID:**
```bash
uv run python cli.py set-truetemperature --room-id 1234567890 --temperature 20.5
```

**Set temperature by room name (case-insensitive):**
```bash
uv run python cli.py set-truetemperature --room-name "Living Room" --temperature 20.5
uv run python cli.py set-truetemperature --room-name "living room" --temperature 19.0
```

## Architecture

The CLI demonstrates best practices with a clean, modular architecture:

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

### Key Patterns

- **Environment-based configuration**: Credentials loaded from environment variables
- **Dependency injection**: Clean separation of concerns with injected dependencies
- **Decorator pattern**: Error handling applied consistently via `@handle_api_errors`
- **Modular design**: CLI, business logic, and presentation cleanly separated
- **Typer CLI framework**: Modern Python CLI with type-safe arguments and automatic help generation
- **Rich formatting**: Beautiful terminal output with tables, panels, and spinners

## Development

The example uses the parent `py-netatmo-truetemp` package as an editable dependency. This means:

- Changes to the parent library are immediately available
- No need to reinstall after modifying library code
- Clean package imports (no relative imports)

### Validation

```bash
# Syntax check all CLI modules
python -m py_compile cli.py helpers.py display.py

# Syntax check library
python -m py_compile ../src/py_netatmo_truetemp/*.py
```

## Files

- `cli.py` - CLI entry point with command definitions
- `helpers.py` - Helper functions (API init, error handling, validation)
- `display.py` - Display formatting with Rich library
- `pyproject.toml` - Example dependencies (Typer, Rich)
- `Taskfile.yml` - Task runner configuration with development and CLI shortcuts
- `README.md` - This file
- `CLAUDE.md` - Detailed development workflow and architecture guide
