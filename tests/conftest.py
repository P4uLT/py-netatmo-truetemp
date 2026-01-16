"""Shared test fixtures and realistic API response data."""

import pytest


# ============================================================================
# API Response Fixtures - Realistic Netatmo API responses
# ============================================================================


@pytest.fixture
def fixture_auth_success():
    """Valid authentication response with session cookie."""
    return {
        "status": "ok",
        "time_server": 1642345678,
    }


@pytest.fixture
def fixture_homesdata_single_home():
    """Realistic homesdata API response with one home and three rooms."""
    return {
        "body": {
            "homes": [
                {
                    "id": "home-123",
                    "name": "My Home",
                    "rooms": [
                        {"id": "room-1", "name": "Living Room"},
                        {"id": "room-2", "name": "Bedroom"},
                        {"id": "room-3", "name": "Kitchen"},
                    ],
                }
            ]
        },
        "status": "ok",
        "time_server": 1642345678,
    }


@pytest.fixture
def fixture_homesdata_multiple_homes():
    """Homesdata response with multiple homes."""
    return {
        "body": {
            "homes": [
                {
                    "id": "home-123",
                    "name": "My Home",
                    "rooms": [
                        {"id": "room-1", "name": "Living Room"},
                    ],
                },
                {
                    "id": "home-456",
                    "name": "Vacation Home",
                    "rooms": [
                        {"id": "room-4", "name": "Guest Room"},
                    ],
                },
            ]
        },
        "status": "ok",
        "time_server": 1642345678,
    }


@pytest.fixture
def fixture_homestatus_with_temps():
    """Homestatus response with room temperatures."""
    return {
        "body": {
            "home": {
                "id": "home-123",
                "rooms": [
                    {"id": "room-1", "therm_measured_temperature": 21.5},
                    {"id": "room-2", "therm_measured_temperature": 19.0},
                    {"id": "room-3", "therm_measured_temperature": 20.3},
                ],
            }
        },
        "status": "ok",
        "time_server": 1642345678,
    }


@pytest.fixture
def fixture_truetemperature_success():
    """Successful temperature update response."""
    return {
        "status": "ok",
        "time_server": 1642345678,
    }


@pytest.fixture
def fixture_api_error_401():
    """Unauthorized error response."""
    return {
        "error": {"code": 1, "message": "Access token expired"},
        "status": "failed",
    }


@pytest.fixture
def fixture_api_error_403():
    """Forbidden error response."""
    return {
        "error": {"code": 3, "message": "Forbidden"},
        "status": "failed",
    }


@pytest.fixture
def fixture_api_error_500():
    """Internal server error response."""
    return {
        "error": {"code": 500, "message": "Internal server error"},
        "status": "failed",
    }


# ============================================================================
# Test Data Builders
# ============================================================================

# Temperature test data
VALID_TEMPS = [-50.0, -10.0, 0.0, 20.0, 50.0]
INVALID_TEMPS = [-50.1, -100.0, 50.1, 100.0]

# ID test data
VALID_IDS = ["abc123", "room-id-123", "12345", "home_id"]
INVALID_IDS = ["", "   ", "  \t\n  "]
