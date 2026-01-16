"""Tests for ThermostatService."""

import pytest
from unittest.mock import Mock

from py_netatmo_truetemp.thermostat_service import ThermostatService
from py_netatmo_truetemp.exceptions import ApiError, ValidationError, RoomNotFoundError


class TestListRoomsWithThermostats:
    """Tests for list_rooms_with_thermostats method."""

    def test_list_rooms_with_thermostats_success(self):
        """Test successful listing of rooms with thermostats."""
        mock_home_service = Mock()
        mock_api_client = Mock()

        mock_home_service.get_default_home_id.return_value = "test-home-id"
        mock_home_service.get_homes_data.return_value = {
            "body": {
                "homes": [
                    {
                        "id": "test-home-id",
                        "rooms": [
                            {"id": "room1", "name": "Living Room"},
                            {"id": "room2", "name": "Bedroom"},
                            {"id": "room3", "name": "Kitchen"},
                        ],
                    }
                ]
            }
        }
        mock_home_service.get_home_status.return_value = {
            "body": {
                "home": {
                    "rooms": [
                        {"id": "room1", "therm_measured_temperature": 21.5},
                        {"id": "room2", "therm_measured_temperature": 19.0},
                        {"id": "room3"},
                    ]
                }
            }
        }

        service = ThermostatService(mock_api_client, mock_home_service)
        result = service.list_rooms_with_thermostats()

        assert len(result) == 2
        assert result[0] == {"id": "room1", "name": "Living Room"}
        assert result[1] == {"id": "room2", "name": "Bedroom"}

    def test_list_rooms_empty_response(self):
        """Test handling of empty room list."""
        mock_home_service = Mock()
        mock_api_client = Mock()

        mock_home_service.get_default_home_id.return_value = "test-home-id"
        mock_home_service.get_homes_data.return_value = {
            "body": {"homes": [{"id": "test-home-id", "rooms": []}]}
        }
        mock_home_service.get_home_status.return_value = {
            "body": {"home": {"rooms": []}}
        }

        service = ThermostatService(mock_api_client, mock_home_service)
        result = service.list_rooms_with_thermostats()

        assert result == []

    def test_list_rooms_no_thermostats(self):
        """Test handling when no rooms have thermostats."""
        mock_home_service = Mock()
        mock_api_client = Mock()

        mock_home_service.get_default_home_id.return_value = "test-home-id"
        mock_home_service.get_homes_data.return_value = {
            "body": {
                "homes": [
                    {
                        "id": "test-home-id",
                        "rooms": [{"id": "room1", "name": "Storage"}],
                    }
                ]
            }
        }
        mock_home_service.get_home_status.return_value = {
            "body": {"home": {"rooms": [{"id": "room1"}]}}
        }

        service = ThermostatService(mock_api_client, mock_home_service)
        result = service.list_rooms_with_thermostats()

        assert result == []

    def test_list_rooms_with_specific_home_id(self):
        """Test listing rooms with specific home ID."""
        mock_home_service = Mock()
        mock_api_client = Mock()

        mock_home_service.get_homes_data.return_value = {
            "body": {
                "homes": [
                    {
                        "id": "specific-home",
                        "rooms": [{"id": "room1", "name": "Office"}],
                    }
                ]
            }
        }
        mock_home_service.get_home_status.return_value = {
            "body": {
                "home": {"rooms": [{"id": "room1", "therm_measured_temperature": 20.0}]}
            }
        }

        service = ThermostatService(mock_api_client, mock_home_service)
        result = service.list_rooms_with_thermostats(home_id="specific-home")

        assert len(result) == 1
        assert result[0] == {"id": "room1", "name": "Office"}
        mock_home_service.get_homes_data.assert_called_once_with(
            home_id="specific-home"
        )
        mock_home_service.get_home_status.assert_called_once_with(
            home_id="specific-home"
        )

    def test_list_rooms_malformed_response(self):
        """Test handling of malformed API response."""
        mock_home_service = Mock()
        mock_api_client = Mock()

        mock_home_service.get_default_home_id.return_value = "test-home-id"
        mock_home_service.get_homes_data.return_value = {"body": {"homes": []}}
        mock_home_service.get_home_status.return_value = {"body": {}}

        service = ThermostatService(mock_api_client, mock_home_service)

        with pytest.raises(ApiError, match="Failed to parse API response"):
            service.list_rooms_with_thermostats()

    def test_list_rooms_missing_room_name(self):
        """Test handling rooms with missing names."""
        mock_home_service = Mock()
        mock_api_client = Mock()

        mock_home_service.get_default_home_id.return_value = "test-home-id"
        mock_home_service.get_homes_data.return_value = {
            "body": {"homes": [{"id": "test-home-id", "rooms": [{"id": "room1"}]}]}
        }
        mock_home_service.get_home_status.return_value = {
            "body": {
                "home": {"rooms": [{"id": "room1", "therm_measured_temperature": 20.0}]}
            }
        }

        service = ThermostatService(mock_api_client, mock_home_service)
        result = service.list_rooms_with_thermostats()

        assert len(result) == 1
        assert result[0] == {"id": "room1", "name": "Room room1"}


class TestSetRoomTemperature:
    """Tests for set_room_temperature method."""

    def test_set_room_temperature_success(self):
        """Test successful temperature setting."""
        # Arrange
        mock_home_service = Mock()
        mock_api_client = Mock()

        # Mock get_homes_data for room name lookup
        mock_home_service.get_homes_data.return_value = {
            "body": {
                "homes": [
                    {
                        "id": "home-123",
                        "rooms": [{"id": "room-1", "name": "Living Room"}],
                    }
                ]
            }
        }

        mock_home_service.get_home_status.return_value = {
            "body": {
                "home": {
                    "rooms": [{"id": "room-1", "therm_measured_temperature": 20.0}]
                }
            },
            "status": "ok",
            "time_server": 1642345678,
        }

        mock_api_client.post_typed.return_value = {
            "status": "ok",
            "time_server": 1642345678,
        }

        service = ThermostatService(mock_api_client, mock_home_service)

        # Act
        service.set_room_temperature(
            room_id="room-1",
            home_id="home-123",
            corrected_temperature=22.0,
        )

        # Assert: Verify API called with correct payload
        mock_api_client.post_typed.assert_called_once()
        call_args = mock_api_client.post_typed.call_args
        assert call_args[0][0] == "/api/truetemperature"
        payload = call_args[1]["json_data"]
        assert payload["room_id"] == "room-1"
        assert payload["home_id"] == "home-123"
        assert payload["corrected_temperature"] == 22.0

    def test_set_temperature_validation_out_of_range(self):
        """Test that out-of-range temperature raises ValidationError."""
        # Arrange
        mock_home_service = Mock()
        mock_api_client = Mock()
        service = ThermostatService(mock_api_client, mock_home_service)

        # Act & Assert
        with pytest.raises(ValidationError, match="must be between"):
            service.set_room_temperature(
                room_id="room-1",
                home_id="home-123",
                corrected_temperature=100.0,  # Out of range
            )

    def test_set_temperature_empty_room_id_raises_error(self):
        """Test that empty room_id raises ValidationError."""
        # Arrange
        mock_home_service = Mock()
        mock_api_client = Mock()
        service = ThermostatService(mock_api_client, mock_home_service)

        # Act & Assert
        with pytest.raises(ValidationError, match="room_id cannot be empty"):
            service.set_room_temperature(
                room_id="",
                home_id="home-123",
                corrected_temperature=20.0,
            )

    def test_set_temperature_room_not_found(self):
        """Test that missing room raises RoomNotFoundError."""
        # Arrange
        mock_home_service = Mock()
        mock_api_client = Mock()

        # Mock get_homes_data for room name lookup
        mock_home_service.get_homes_data.return_value = {
            "body": {
                "homes": [
                    {
                        "id": "home-123",
                        "rooms": [{"id": "room-2", "name": "Other Room"}],
                    }
                ]
            }
        }

        # Return status without the requested room
        mock_home_service.get_home_status.return_value = {
            "body": {
                "home": {
                    "rooms": [{"id": "room-2", "therm_measured_temperature": 20.0}]
                }
            }
        }

        service = ThermostatService(mock_api_client, mock_home_service)

        # Act & Assert
        with pytest.raises(RoomNotFoundError, match="room-1"):
            service.set_room_temperature(
                room_id="room-1",
                home_id="home-123",
                corrected_temperature=22.0,
            )
