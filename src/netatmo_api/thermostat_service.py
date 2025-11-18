"""Thermostat operations and temperature control."""

from typing import Any

from .api_client import NetatmoApiClient
from .constants import ApiEndpoints
from .exceptions import RoomNotFoundError
from .home_service import HomeService
from .logger import setup_logger
from .validators import (
    validate_home_id,
    validate_room_id,
    validate_temperature,
)

logger = setup_logger(__name__)


class ThermostatService:
    """Provides thermostat control and temperature management."""

    def __init__(self, api_client: NetatmoApiClient, home_service: HomeService):
        self.api_client = api_client
        self.home_service = home_service

    def _get_room_name(self, home_id: str, room_id: str) -> str:
        try:
            homes_data = self.home_service.get_homes_data()
            for home in homes_data["body"]["homes"]:
                if str(home["id"]) == str(home_id):
                    for room in home.get("rooms", []):
                        if str(room["id"]) == str(room_id):
                            return room.get("name", room_id)
            return room_id
        except (KeyError, IndexError):
            return room_id

    def set_room_temperature(
        self, room_id: str, corrected_temperature: float, home_id: str | None = None
    ) -> dict[str, Any]:
        """Sets calibrated temperature for a room.

        Raises:
            ValidationError: If room_id, temperature, or home_id is invalid
            RoomNotFoundError: If the room is not found
            ApiError: If the API request fails
        """
        validate_room_id(room_id)
        validate_temperature(corrected_temperature, "corrected_temperature")
        if home_id is not None:
            validate_home_id(home_id)

        if home_id is None:
            home_id = self.home_service.get_default_home_id()

        # Get room name from homesdata (contains room metadata)
        # This is only used for logging, so we'll fall back to room_id if it fails
        try:
            room_name = self._get_room_name(home_id, room_id)
        except Exception as e:
            logger.debug(f"Could not fetch room name: {e}")
            room_name = room_id  # Fallback to ID

        # Get current home status to find room's measured temperature
        status_response = self.home_service.get_home_status(home_id=home_id)

        try:
            home = status_response["body"]["home"]
            rooms = home["rooms"]

            # Find the room and get current measured temperature
            current_temperature = None
            room_found = False
            logger.debug(f"Looking for room_id {room_id} in {len(rooms)} rooms")
            for room in rooms:
                logger.debug(f"  Room: id={room.get('id')}, name={room_name}")
                if str(room["id"]) == str(room_id):
                    room_found = True
                    current_temperature = room["therm_measured_temperature"]
                    logger.info(
                        f"Found room {room_name}: "
                        f"current={current_temperature}°C, "
                        f"target={corrected_temperature}°C"
                    )
                    break

            if not room_found:
                logger.error(f"Room {room_id} not found in home status")
                raise RoomNotFoundError(room_id)

            if current_temperature is None:
                logger.error(f"Could not get current temperature for room {room_id}")
                raise RoomNotFoundError(room_id)

            # Check if temperature is already at target (within 0.1°C tolerance)
            if abs(current_temperature - corrected_temperature) < 0.1:
                logger.info(
                    f"Room {room_name} temperature already at target "
                    f"({current_temperature}°C), skipping API call"
                )
                return {
                    "status": "ok",
                    "time_server": status_response.get("time_server"),
                }

            # Warn about large temperature differences
            temp_diff = abs(current_temperature - corrected_temperature)
            if temp_diff > 10.0:
                logger.warning(
                    f"Large temperature difference detected: {temp_diff:.1f}°C. "
                    f"Current: {current_temperature}°C, Corrected: {corrected_temperature}°C"
                )

            # Set the true temperature
            payload = {
                "home_id": home_id,
                "room_id": room_id,
                "current_temperature": current_temperature,
                "corrected_temperature": corrected_temperature,
            }

            response = self.api_client.post(
                ApiEndpoints.TRUE_TEMPERATURE, json_data=payload
            )

            logger.info(
                f"Set temperature for room {room_id} to {corrected_temperature}°C"
            )

            return response

        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing home status: {e}")
            raise RoomNotFoundError(room_id) from e
