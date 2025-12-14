#!/usr/bin/env python3
"""Tests for CLI commands."""

from unittest.mock import Mock, patch

from typer.testing import CliRunner

from cli import app

runner = CliRunner()


class TestListRoomsCommand:
    """Tests for list-rooms command."""

    @patch("cli.create_netatmo_api_with_spinner")
    def test_list_rooms_success(self, mock_create_api):
        """Test successful room listing."""
        mock_api = Mock()
        mock_api.list_thermostat_rooms.return_value = [
            {"id": "123", "name": "Living Room"},
            {"id": "456", "name": "Bedroom"},
        ]
        mock_create_api.return_value = mock_api

        result = runner.invoke(app, ["list-rooms"])

        assert result.exit_code == 0
        assert "Living Room" in result.stdout
        assert "Bedroom" in result.stdout


class TestSetTruetemperatureCommand:
    """Tests for set-truetemperature command."""

    @patch("cli.create_netatmo_api_with_spinner")
    @patch("cli.resolve_room_id")
    def test_set_temperature_by_name(self, mock_resolve, mock_create_api):
        """Test setting temperature by room name."""
        mock_api = Mock()
        mock_create_api.return_value = mock_api
        mock_resolve.return_value = ("123", "Living Room")

        result = runner.invoke(
            app, ["set-truetemperature", "--room-name", "Living Room", "--temperature", "20.5"]
        )

        assert result.exit_code == 0
        mock_api.set_truetemperature.assert_called_once_with(
            room_id="123",
            corrected_temperature=20.5,
            home_id=None,
        )

    def test_set_temperature_missing_parameters(self):
        """Test error when required parameters missing."""
        result = runner.invoke(app, ["set-truetemperature", "--temperature", "20.5"])

        assert result.exit_code == 1
