"""Tests for input validators."""

import pytest

from py_netatmo_truetemp.validators import (
    validate_temperature,
)
from py_netatmo_truetemp.exceptions import ValidationError
from tests.conftest import VALID_TEMPS, INVALID_TEMPS


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
