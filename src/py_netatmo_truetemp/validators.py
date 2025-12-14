"""Input validation helpers for Netatmo API."""

from .constants import TemperatureLimits
from .exceptions import ValidationError


def validate_temperature(temperature: float, param_name: str = "temperature") -> None:
    """Validate temperature is within acceptable range.

    Args:
        temperature: Temperature value to validate
        param_name: Name of the parameter (for error messages)

    Raises:
        ValidationError: If temperature is out of range
    """
    if (
        not TemperatureLimits.MIN_CELSIUS
        <= temperature
        <= TemperatureLimits.MAX_CELSIUS
    ):
        raise ValidationError(
            f"{param_name} must be between {TemperatureLimits.MIN_CELSIUS}°C "
            f"and {TemperatureLimits.MAX_CELSIUS}°C, got {temperature}°C"
        )


def validate_room_id(room_id: str) -> None:
    """Validate room ID is not empty.

    Args:
        room_id: Room ID to validate

    Raises:
        ValidationError: If room_id is empty or whitespace only
    """
    if not room_id or not room_id.strip():
        raise ValidationError("room_id cannot be empty")


def validate_home_id(home_id: str) -> None:
    """Validate home ID is not empty.

    Args:
        home_id: Home ID to validate

    Raises:
        ValidationError: If home_id is empty or whitespace only
    """
    if not home_id or not home_id.strip():
        raise ValidationError("home_id cannot be empty")
