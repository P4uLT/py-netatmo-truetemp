#!/usr/bin/env python3
"""CLI example for py-netatmo-truetemp library."""

import os

import click

from py_netatmo_truetemp import NetatmoAPI
from py_netatmo_truetemp.logger import setup_logger

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
@click.command()
@click.option("--room-id", required=True, help="Room ID to set temperature for")
@click.option(
    "--temperature", type=float, required=True, help="Corrected temperature value"
)
@click.option(
    "--home-id", default=None, help="Home ID (optional, uses default if not provided)"
)
def main(room_id: str, temperature: float, home_id: str | None = None):
    """Sets calibrated temperature for a Netatmo room.

    Example:
        python netatmo.py --room-id 2631283693 --temperature 20.5
    """
    try:
        # Create API client (Dependency Inversion)
        api = create_netatmo_api()

        # Create service with injected API (Dependency Inversion)
        service = NetatmoService(api)

        # Execute operation
        service.set_room_temperature(
            room_id=room_id, corrected_temperature=temperature, home_id=home_id
        )
        click.echo(f"Successfully set temperature to {temperature}°C")

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
