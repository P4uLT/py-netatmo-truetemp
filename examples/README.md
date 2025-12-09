# Netatmo CLI Example

Example CLI application demonstrating how to use the `py-netatmo-truetemp` library.

## Setup

### 1. Create Virtual Environment

```bash
cd example
uv venv
```

### 2. Install Dependencies

This will install the parent package as an editable dependency along with CLI dependencies:

```bash
uv sync
```

### 3. Configure Environment

Edit `.mise.local.toml` with your Netatmo credentials:

```toml
[env]
NETATMO_USERNAME = "your.email@example.com"
NETATMO_PASSWORD = "your-password"
NETATMO_HOME_ID = "your-home-id"
```

## Usage

### Direct CLI Usage

```bash
uv run python cli.py --room-id <room_id> --temperature <temp>
```

Example:
```bash
uv run python cli.py --room-id 2631283693 --temperature 20.5
```

### Using Task Runner

Pre-configured tasks are available via [Task](https://taskfile.dev):

```bash
# Set temperature for Bureau
task bureau TEMP=20.5

# Set temperature for Salle à manger
task salle-a-manger TEMP=21.0

# Set temperature for Chambre Liam
task chambre-liam TEMP=19.3

# Set temperature for Couloir
task couloir TEMP=18.5

# Set temperature for custom room
task set-temp ROOM_ID=<room_id> TEMP=20.0

# List all tasks
task list
```

## Architecture

This example demonstrates:

- **Environment-based configuration**: Credentials loaded from environment variables
- **Dependency injection**: Clean separation of concerns with injected dependencies
- **Service layer pattern**: Business logic separated from API calls
- **Proper error handling**: Graceful error messages and logging
- **Click CLI framework**: Modern Python CLI with options and validation

## Development

The example uses the parent `py-netatmo-truetemp` package as an editable dependency. This means:

- Changes to the parent library are immediately available
- No need to reinstall after modifying library code
- Clean package imports (no relative imports)

## Files

- `cli.py` - CLI entry point
- `pyproject.toml` - Example dependencies and configuration
- `.mise.local.toml` - Environment variables for Netatmo API
- `Taskfile.yml` - Task runner configuration for common operations
- `README.md` - This file
