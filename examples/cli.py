#!/usr/bin/env python3
"""CLI example for py-netatmo-truetemp library."""

import os
import sys

import click
from rich.console import Console
from rich.table import Table

from py_netatmo_truetemp import NetatmoAPI
from py_netatmo_truetemp.exceptions import (
    AuthenticationError,
    ApiError,
    NetatmoError,
    ValidationError,
    RoomNotFoundError,
    HomeNotFoundError,
)
from py_netatmo_truetemp.logger import setup_logger

console = Console()

logger = setup_logger(__name__)


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

        # Check for missing required variables
        missing = [key for key, value in required_vars.items() if not value]
        if missing:
            raise ValueError(
                f"Missing required environment variables: "
                f"{', '.join(k.upper() for k in missing)}"
            )

        # Optional configuration
        optional_config = {
            "scopes": os.environ.get(
                "NETATMO_SCOPES",
                "read_station read_thermostat write_thermostat read_camera "
                "write_camera access_camera read_presence access_presence "
                "read_smokedetector read_homecoach",
            ),
            "home_id": os.environ.get("NETATMO_HOME_ID"),
        }

        return {**required_vars, **optional_config}


class NetatmoService:
    """Provides business logic for Netatmo operations."""

    def __init__(self, api: NetatmoAPI):
        self.api = api

    def list_thermostat_rooms(self, home_id: str | None = None) -> list[dict[str, str]]:
        """Lists all rooms with thermostats."""
        logger.info("Fetching rooms with thermostats")
        return self.api.list_thermostat_rooms(home_id=home_id)

    def set_room_temperature(
        self, room_id: str, corrected_temperature: float, home_id: str | None = None
    ) -> dict:
        """Sets calibrated temperature for a room."""
        logger.info(
            f"Setting temperature for room {room_id} to {corrected_temperature}°C"
        )

        response = self.api.set_truetemperature(
            room_id=room_id,
            corrected_temperature=corrected_temperature,
            home_id=home_id,
        )

        if response.get("status") == "failed":
            logger.error(f"Failed to set temperature: {response.get('error')}")
        else:
            logger.info(f"Successfully set temperature for room {room_id}")

        return response


def create_netatmo_api() -> NetatmoAPI:
    """Creates configured NetatmoAPI instance.

    Raises:
        ValueError: If configuration is invalid
    """
    config = NetatmoConfig.from_environment()

    return NetatmoAPI(
        username=config["username"],
        password=config["password"],
        scopes=config["scopes"],
        home_id=config.get("home_id"),
    )


# CLI Interface
@click.group()
def cli():
    """Netatmo thermostat control CLI."""
    pass


@cli.command(name="list-rooms")
@click.option(
    "--home-id", default=None, help="Home ID (optional, uses default if not provided)"
)
def list_rooms(home_id: str | None = None):
    """Lists all rooms with thermostats.

    Example:
        python cli.py list-rooms
        python cli.py list-rooms --home-id <home_id>
    """
    try:
        api = create_netatmo_api()
        service = NetatmoService(api)

        rooms = service.list_thermostat_rooms(home_id=home_id)

        if not rooms:
            console.print("[yellow]No rooms with thermostats found.[/yellow]")
            return

        table = Table(title=f"Thermostat Rooms ({len(rooms)} found)")
        table.add_column("Room ID", style="cyan", no_wrap=True)
        table.add_column("Room Name", style="green")

        for room in rooms:
            table.add_row(room['id'], room['name'])

        console.print(table)

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        console.print(f"[red]Configuration error:[/red] {e}", file=sys.stderr)
        raise click.Abort()
    except AuthenticationError as e:
        logger.error(f"Authentication error: {e}")
        console.print(
            "[red]Authentication failed.[/red] Check credentials in .mise.local.toml",
            file=sys.stderr
        )
        raise click.Abort()
    except (HomeNotFoundError, RoomNotFoundError) as e:
        logger.error(f"Resource not found: {e}")
        console.print(f"[red]Not found:[/red] {e}", file=sys.stderr)
        raise click.Abort()
    except ApiError as e:
        logger.error(f"API error: {e}")
        console.print(f"[red]API error:[/red] {e}", file=sys.stderr)
        raise click.Abort()
    except NetatmoError as e:
        logger.error(f"Netatmo error: {e}")
        console.print(f"[red]Netatmo error:[/red] {e}", file=sys.stderr)
        raise click.Abort()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        console.print(f"[red]Unexpected error:[/red] {e}", file=sys.stderr)
        raise click.Abort()


@cli.command(name="set-temperature")
@click.option("--room-id", default=None, help="Room ID to set temperature for")
@click.option("--room-name", default=None, help="Room name to set temperature for (alternative to --room-id)")
@click.option(
    "--temperature", type=float, required=True, help="Corrected temperature value"
)
@click.option(
    "--home-id", default=None, help="Home ID (optional, uses default if not provided)"
)
def set_temperature(room_id: str | None, room_name: str | None, temperature: float, home_id: str | None = None):
    """Sets calibrated temperature for a Netatmo room.

    Example:
        python cli.py set-temperature --room-id 2631283693 --temperature 20.5
        python cli.py set-temperature --room-name "Bureau" --temperature 20.5
    """
    try:
        if not room_id and not room_name:
            console.print("[red]Error:[/red] Either --room-id or --room-name must be provided", file=sys.stderr)
            raise click.Abort()

        if room_id and room_name:
            console.print("[red]Error:[/red] Cannot use both --room-id and --room-name", file=sys.stderr)
            raise click.Abort()

        api = create_netatmo_api()
        service = NetatmoService(api)

        if room_name:
            rooms = service.list_thermostat_rooms(home_id=home_id)
            matching_rooms = [r for r in rooms if r['name'].lower() == room_name.lower()]

            if not matching_rooms:
                console.print(f"[red]Error:[/red] Room '{room_name}' not found", file=sys.stderr)
                raise click.Abort()

            if len(matching_rooms) > 1:
                console.print(f"[yellow]Warning:[/yellow] Multiple rooms named '{room_name}' found, using first match")

            room_id = matching_rooms[0]['id']
            logger.info(f"Found room: {room_name} (ID: {room_id})")

        service.set_room_temperature(
            room_id=room_id, corrected_temperature=temperature, home_id=home_id
        )
        console.print(f"[green]✓[/green] Successfully set temperature to {temperature}°C")

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        console.print(f"[red]Configuration error:[/red] {e}", file=sys.stderr)
        raise click.Abort()
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        console.print(f"[red]Validation error:[/red] {e}", file=sys.stderr)
        raise click.Abort()
    except AuthenticationError as e:
        logger.error(f"Authentication error: {e}")
        console.print(
            "[red]Authentication failed.[/red] Check credentials in .mise.local.toml",
            file=sys.stderr
        )
        raise click.Abort()
    except (HomeNotFoundError, RoomNotFoundError) as e:
        logger.error(f"Resource not found: {e}")
        console.print(f"[red]Not found:[/red] {e}", file=sys.stderr)
        raise click.Abort()
    except ApiError as e:
        logger.error(f"API error: {e}")
        console.print(f"[red]API error:[/red] {e}", file=sys.stderr)
        raise click.Abort()
    except NetatmoError as e:
        logger.error(f"Netatmo error: {e}")
        console.print(f"[red]Netatmo error:[/red] {e}", file=sys.stderr)
        raise click.Abort()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        console.print(f"[red]Unexpected error:[/red] {e}", file=sys.stderr)
        raise click.Abort()


if __name__ == "__main__":
    cli()
