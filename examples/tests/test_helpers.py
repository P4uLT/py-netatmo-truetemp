#!/usr/bin/env python3
"""Tests for helper functions."""

from unittest.mock import Mock

import pytest

from helpers import NetatmoConfig, resolve_room_id, validate_room_input


class TestNetatmoConfig:
    """Tests for NetatmoConfig class."""

    def test_from_environment_success(self, monkeypatch):
        """Test successful configuration loading."""
        monkeypatch.setenv("NETATMO_USERNAME", "test@example.com")
        monkeypatch.setenv("NETATMO_PASSWORD", "testpass")

        config = NetatmoConfig.from_environment()

        assert config["username"] == "test@example.com"
        assert config["password"] == "testpass"
        assert "home_id" in config

    def test_from_environment_missing_username(self, monkeypatch):
        """Test error when username is missing."""
        monkeypatch.delenv("NETATMO_USERNAME", raising=False)
        monkeypatch.setenv("NETATMO_PASSWORD", "testpass")

        with pytest.raises(ValueError, match="Missing required environment variables"):
            NetatmoConfig.from_environment()

    def test_from_environment_with_optional_home_id(self, monkeypatch):
        """Test configuration with optional home_id."""
        monkeypatch.setenv("NETATMO_USERNAME", "test@example.com")
        monkeypatch.setenv("NETATMO_PASSWORD", "testpass")
        monkeypatch.setenv("NETATMO_HOME_ID", "home123")

        config = NetatmoConfig.from_environment()

        assert config["home_id"] == "home123"


class TestResolveRoomId:
    """Tests for resolve_room_id function."""

    def test_resolve_by_name_case_insensitive(self):
        """Test room name resolution is case-insensitive."""
        mock_api = Mock()
        mock_api.list_thermostat_rooms.return_value = [
            {"id": "123", "name": "Living Room"},
            {"id": "456", "name": "Bedroom"},
        ]

        room_id, room_name = resolve_room_id(mock_api, None, "living room", None)

        assert room_id == "123"
        assert room_name == "Living Room"

    def test_resolve_by_id(self):
        """Test direct room ID resolution."""
        mock_api = Mock()
        mock_api.list_thermostat_rooms.return_value = [
            {"id": "123", "name": "Living Room"},
            {"id": "456", "name": "Bedroom"},
        ]

        room_id, room_name = resolve_room_id(mock_api, "456", None, None)

        assert room_id == "456"
        assert room_name == "Bedroom"


class TestValidateRoomInput:
    """Tests for validate_room_input function."""

    def test_validate_with_room_id(self):
        """Test validation passes with room_id."""
        # Should not raise
        validate_room_input("123", None)

    def test_validate_with_room_name(self):
        """Test validation passes with room_name."""
        # Should not raise
        validate_room_input(None, "Living Room")

    def test_validate_fails_without_inputs(self):
        """Test validation fails when neither parameter provided."""
        import typer

        with pytest.raises(typer.Exit):
            validate_room_input(None, None)

    def test_validate_fails_with_both_inputs(self):
        """Test validation fails when both parameters provided."""
        import typer

        with pytest.raises(typer.Exit):
            validate_room_input("123", "Living Room")
