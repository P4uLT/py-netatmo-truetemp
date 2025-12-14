#!/usr/bin/env python3
"""Helper functions for CLI operations."""

import functools
import os

import typer
from py_netatmo_truetemp import NetatmoAPI
from py_netatmo_truetemp.exceptions import (
    ApiError,
    AuthenticationError,
    HomeNotFoundError,
    NetatmoError,
    RoomNotFoundError,
    ValidationError,
)
from rich.console import Console
from rich.status import Status

console = Console()
error_console = Console(stderr=True)


class NetatmoConfig:
    """Loads and validates Netatmo configuration from environment variables."""

    @staticmethod
    def from_environment() -> dict:
        """Loads Netatmo configuration from environment variables.

        Raises:
            ValueError: If required environment variables are missing
        """
        required_vars = {
            "username": os.environ.get("NETATMO_USERNAME"),
            "password": os.environ.get("NETATMO_PASSWORD"),
        }

        missing = [key for key, value in required_vars.items() if not value]
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(k.upper() for k in missing)}"
            )

        optional_config = {
            "home_id": os.environ.get("NETATMO_HOME_ID"),
        }

        return {**required_vars, **optional_config}


def create_netatmo_api_with_spinner() -> NetatmoAPI:
    """Creates configured NetatmoAPI instance with loading spinner.

    Raises:
        ValueError: If configuration is invalid
    """
    config = NetatmoConfig.from_environment()

    with Status("[bold green]Connecting to Netatmo...", console=console):
        api = NetatmoAPI(
            username=config["username"],
            password=config["password"],
            home_id=config.get("home_id"),
        )

    return api


def handle_api_errors(func):
    """Decorator for consistent error handling across CLI commands."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except typer.Exit:
            raise
        except ValueError as e:
            from display import display_error_panel

            display_error_panel("Configuration Error", str(e))
            raise typer.Exit(code=1)
        except ValidationError as e:
            from display import display_error_panel

            display_error_panel("Validation Error", str(e))
            raise typer.Exit(code=1)
        except AuthenticationError as e:
            from display import display_error_panel

            display_error_panel("Authentication Failed", f"{e}\n\nCheck your credentials")
            raise typer.Exit(code=1)
        except (HomeNotFoundError, RoomNotFoundError) as e:
            from display import display_error_panel

            display_error_panel("Not Found", str(e))
            raise typer.Exit(code=1)
        except ApiError as e:
            from display import display_error_panel

            display_error_panel("API Error", str(e))
            raise typer.Exit(code=1)
        except NetatmoError as e:
            from display import display_error_panel

            display_error_panel("Netatmo Error", str(e))
            raise typer.Exit(code=1)
        except Exception as e:
            from display import display_error_panel

            display_error_panel("Unexpected Error", str(e))
            raise typer.Exit(code=1)

    return wrapper


def resolve_room_id(
    api: NetatmoAPI, room_id: str | None, room_name: str | None, home_id: str | None
) -> tuple[str, str]:
    """Resolves room ID from name or validates direct ID.

    Args:
        api: NetatmoAPI instance
        room_id: Direct room ID (if provided)
        room_name: Room name to look up (if provided)
        home_id: Optional home ID

    Returns:
        Tuple of (room_id, room_name)

    Raises:
        RoomNotFoundError: If room name or ID doesn't match any room
    """
    rooms = api.list_thermostat_rooms(home_id=home_id)

    if room_name:
        matching = [r for r in rooms if r["name"].lower() == room_name.lower()]

        if not matching:
            raise RoomNotFoundError(room_name)

        if len(matching) > 1:
            console.print(
                f"[yellow]Warning:[/yellow] Multiple rooms named '{room_name}', using first"
            )

        return matching[0]["id"], matching[0]["name"]

    room = next((r for r in rooms if r["id"] == room_id), None)
    if not room:
        raise RoomNotFoundError(room_id)

    return room_id, room["name"]


def validate_room_input(room_id: str | None, room_name: str | None) -> None:
    """Validates room input parameters.

    Args:
        room_id: Room ID parameter
        room_name: Room name parameter

    Raises:
        typer.Exit: If validation fails
    """
    if not room_id and not room_name:
        error_console.print("[red]Error:[/red] Either --room-id or --room-name must be provided")
        raise typer.Exit(code=1)

    if room_id and room_name:
        error_console.print("[red]Error:[/red] Cannot use both --room-id and --room-name")
        raise typer.Exit(code=1)
