#!/usr/bin/env python3
"""Pytest configuration and fixtures."""

from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_netatmo_api():
    """Creates a mock NetatmoAPI instance."""
    api = Mock()
    api.list_thermostat_rooms.return_value = [
        {"id": "123", "name": "Living Room"},
        {"id": "456", "name": "Bedroom"},
        {"id": "789", "name": "Kitchen"},
    ]
    return api


@pytest.fixture
def sample_rooms():
    """Returns sample room data."""
    return [
        {"id": "123", "name": "Living Room"},
        {"id": "456", "name": "Bedroom"},
        {"id": "789", "name": "Kitchen"},
    ]


@pytest.fixture
def clean_environment(monkeypatch):
    """Provides a clean environment without Netatmo variables."""
    monkeypatch.delenv("NETATMO_USERNAME", raising=False)
    monkeypatch.delenv("NETATMO_PASSWORD", raising=False)
    monkeypatch.delenv("NETATMO_HOME_ID", raising=False)
