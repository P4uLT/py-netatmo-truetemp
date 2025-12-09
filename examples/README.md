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

This will install the parent package as an editable dependency along with CLI dependencies (Click, Rich):

```bash
uv sync
```

### 3. Configure Environment

Edit `.mise.local.toml` with your Netatmo credentials:

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

## Usage

### Method 1: Direct CLI Execution

**List all rooms with thermostats:**
```bash
uv run python cli.py list-rooms
```

**Set temperature by room ID:**
```bash
uv run python cli.py set-truetemperature --room-id 2631283693 --temperature 20.5
```

**Set temperature by room name (case-insensitive):**
```bash
uv run python cli.py set-truetemperature --room-name "Bureau" --temperature 20.5
uv run python cli.py set-truetemperature --room-name "bureau" --temperature 19.0
```

### Method 2: Using Task Runner

Pre-configured tasks are available via [Task](https://taskfile.dev):

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

## Architecture

The CLI demonstrates best practices with a clean, modular architecture:

### Module Organization

**`cli.py`** - Application entry point:
- Click command group definition (`list-rooms`, `set-temperature`)
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
- **Click CLI framework**: Modern Python CLI with type-safe arguments and validation
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
- `pyproject.toml` - Example dependencies (Click, Rich)
- `.mise.local.toml` - Environment variables for Netatmo API
- `Taskfile.yml` - Task runner configuration for common operations
- `README.md` - This file
- `CLAUDE.md` - Detailed development workflow and architecture guide
