"""Tests for custom exception hierarchy."""

import pytest

from py_netatmo_truetemp.exceptions import (
    NetatmoError,
    AuthenticationError,
    ApiError,
    ValidationError,
    RoomNotFoundError,
    HomeNotFoundError,
)


class TestExceptionHierarchy:
    """Tests for exception inheritance structure."""

    def test_authentication_error_is_netatmo_error(self):
        """Test AuthenticationError inherits from NetatmoError."""
        error = AuthenticationError("Test error")
        assert isinstance(error, NetatmoError)

    def test_api_error_is_netatmo_error(self):
        """Test ApiError inherits from NetatmoError."""
        error = ApiError("Test error", 500)
        assert isinstance(error, NetatmoError)

    def test_validation_error_is_netatmo_error(self):
        """Test ValidationError inherits from NetatmoError."""
        error = ValidationError("Test error")
        assert isinstance(error, NetatmoError)

    def test_room_not_found_is_netatmo_error(self):
        """Test RoomNotFoundError inherits from NetatmoError."""
        error = RoomNotFoundError("room-123")
        assert isinstance(error, NetatmoError)

    def test_home_not_found_is_netatmo_error(self):
        """Test HomeNotFoundError inherits from NetatmoError."""
        error = HomeNotFoundError("home-123")
        assert isinstance(error, NetatmoError)

    def test_catch_all_with_base_exception(self):
        """Test that all exceptions can be caught with NetatmoError."""
        exceptions = [
            AuthenticationError("auth"),
            ApiError("api", 404),
            ValidationError("validation"),
            RoomNotFoundError("room-1"),
            HomeNotFoundError("home-1"),
        ]

        for exc in exceptions:
            with pytest.raises(NetatmoError):
                raise exc


class TestExceptionMessages:
    """Tests for exception message formatting."""

    def test_room_not_found_includes_room_id(self):
        """Test RoomNotFoundError message includes room ID."""
        error = RoomNotFoundError("room-123")
        assert "room-123" in str(error)
        assert error.room_id == "room-123"

    def test_home_not_found_includes_home_id(self):
        """Test HomeNotFoundError message includes home ID."""
        error = HomeNotFoundError("home-456")
        assert "home-456" in str(error)
        assert error.home_id == "home-456"

    def test_home_not_found_without_id(self):
        """Test HomeNotFoundError message when no home ID provided."""
        error = HomeNotFoundError()
        assert "No homes found" in str(error)
        assert error.home_id is None

    def test_api_error_includes_status_code(self):
        """Test ApiError stores status code."""
        error = ApiError("Not found", 404)
        assert error.status_code == 404
        assert "Not found" in str(error)

    def test_api_error_without_status_code(self):
        """Test ApiError without status code."""
        error = ApiError("Generic error")
        assert error.status_code is None
