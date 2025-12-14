"""Tests for ThermostatService."""

import pytest
from unittest.mock import Mock

from py_netatmo_truetemp.thermostat_service import ThermostatService
from py_netatmo_truetemp.exceptions import ApiError


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
