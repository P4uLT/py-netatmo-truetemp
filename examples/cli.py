#!/usr/bin/env python3
"""CLI example for py-netatmo-truetemp library."""

from typing import Annotated

import typer

from helpers import (
    create_netatmo_api_with_spinner,
    handle_api_errors,
    resolve_room_id,
    validate_room_input,
)
from display import (
    display_rooms_table,
    display_temperature_result,
)


app = typer.Typer(
    help="""Netatmo thermostat control CLI.

Examples:

  python cli.py list-rooms

  python cli.py set-truetemperature --room-name "Living Room" --temperature 20.5
"""
)


@app.command(name="list-rooms")
@handle_api_errors
def list_rooms(
    home_id: Annotated[
        str | None,
        typer.Option(help="Home ID (optional, uses default if not provided)")
    ] = None
) -> None:
    """Lists all rooms with thermostats.

    Example:

      python cli.py list-rooms

      python cli.py list-rooms --home-id <home_id>
    """
    api = create_netatmo_api_with_spinner()
    rooms = api.list_thermostat_rooms(home_id=home_id)
    display_rooms_table(rooms)


@app.command(name="set-truetemperature")
@handle_api_errors
def set_truetemperature(
    temperature: Annotated[float, typer.Option(help="Corrected temperature value")],
    room_id: Annotated[
        str | None,
        typer.Option(help="Room ID to set temperature for")
    ] = None,
    room_name: Annotated[
        str | None,
        typer.Option(help="Room name to set temperature for (alternative to --room-id)")
    ] = None,
    home_id: Annotated[
        str | None,
        typer.Option(help="Home ID (optional, uses default if not provided)")
    ] = None
) -> None:
    """Sets calibrated temperature for a Netatmo room.

    Example:

      python cli.py set-truetemperature --room-id 1234567890 --temperature 20.5

      python cli.py set-truetemperature --room-name "Living Room" --temperature 20.5
    """
    validate_room_input(room_id, room_name)

    api = create_netatmo_api_with_spinner()
    resolved_id, resolved_name = resolve_room_id(api, room_id, room_name, home_id)

    api.set_truetemperature(
        room_id=resolved_id,
        corrected_temperature=temperature,
        home_id=home_id,
    )

    display_temperature_result(resolved_name, temperature)


if __name__ == "__main__":
    app()
