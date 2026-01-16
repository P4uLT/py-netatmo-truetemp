"""Tests for input validators."""

import pytest

from py_netatmo_truetemp.validators import (
    validate_temperature,
    validate_room_id,
    validate_home_id,
)
from py_netatmo_truetemp.exceptions import ValidationError
from tests.conftest import VALID_TEMPS, INVALID_TEMPS, VALID_IDS, INVALID_IDS


class TestTemperatureValidation:
    """Tests for temperature range validation."""

    @pytest.mark.parametrize("temp", VALID_TEMPS)
    def test_valid_temperatures_pass(self, temp):
        """Test that valid temperatures pass validation."""
        # Should not raise
        validate_temperature(temp)

    @pytest.mark.parametrize("temp", INVALID_TEMPS)
    def test_invalid_temperatures_raise_error(self, temp):
        """Test that out-of-range temperatures raise ValidationError."""
        with pytest.raises(ValidationError, match="must be between -50.0°C and 50.0°C"):
            validate_temperature(temp)

    def test_boundary_temperatures_valid(self):
        """Test that exact boundary values are valid."""
        validate_temperature(-50.0)  # Min boundary
        validate_temperature(50.0)  # Max boundary

    def test_just_outside_boundaries_invalid(self):
        """Test values just outside boundaries are invalid."""
        with pytest.raises(ValidationError):
            validate_temperature(-50.1)
        with pytest.raises(ValidationError):
            validate_temperature(50.1)

    def test_zero_temperature_valid(self):
        """Test that 0°C is valid."""
        validate_temperature(0.0)

    def test_non_numeric_temperature_raises_type_error(self):
        """Test that non-numeric values raise TypeError."""
        with pytest.raises(TypeError):
            validate_temperature("20.5")  # type: ignore
        with pytest.raises(TypeError):
            validate_temperature(None)  # type: ignore


class TestIDValidation:
    """Tests for ID validation."""

    @pytest.mark.parametrize("room_id", VALID_IDS)
    def test_valid_room_ids_pass(self, room_id):
        """Test that valid room IDs pass validation."""
        validate_room_id(room_id)

    @pytest.mark.parametrize("room_id", INVALID_IDS)
    def test_invalid_room_ids_raise_error(self, room_id):
        """Test that empty/whitespace room IDs raise ValidationError."""
        with pytest.raises(ValidationError, match="room_id cannot be empty"):
            validate_room_id(room_id)

    @pytest.mark.parametrize("home_id", VALID_IDS)
    def test_valid_home_ids_pass(self, home_id):
        """Test that valid home IDs pass validation."""
        validate_home_id(home_id)

    @pytest.mark.parametrize("home_id", INVALID_IDS)
    def test_invalid_home_ids_raise_error(self, home_id):
        """Test that empty/whitespace home IDs raise ValidationError."""
        with pytest.raises(ValidationError, match="home_id cannot be empty"):
            validate_home_id(home_id)

    def test_none_room_id_raises_validation_error(self):
        """Test that None room_id raises ValidationError."""
        with pytest.raises(ValidationError, match="room_id cannot be empty"):
            validate_room_id(None)  # type: ignore

    def test_numeric_id_raises_attribute_error(self):
        """Test that numeric IDs raise AttributeError."""
        with pytest.raises(AttributeError):
            validate_room_id(123)  # type: ignore
