"""Tests for NetatmoApiClient."""

import responses
import pytest
import requests
from unittest.mock import Mock

from py_netatmo_truetemp.api_client import NetatmoApiClient
from py_netatmo_truetemp.auth_manager import AuthenticationManager
from py_netatmo_truetemp.exceptions import ApiError


class TestNetworkErrors:
    """Tests for network error handling."""

    def test_connection_error_raises_api_error(self):
        """Test that connection errors are wrapped in ApiError."""
        # Arrange
        mock_auth_manager = Mock(spec=AuthenticationManager)
        mock_auth_manager.get_auth_headers.return_value = {
            "Authorization": "Bearer test-token"
        }

        api_client = NetatmoApiClient(
            endpoint="https://api.netatmo.com",
            auth_manager=mock_auth_manager,
        )

        # Mock connection error
        with responses.RequestsMock() as rsps:
            rsps.get(
                "https://api.netatmo.com/api/test",
                body=requests.ConnectionError("Connection refused"),
            )

            # Act & Assert
            with pytest.raises(ApiError, match="Network error"):
                api_client.get("/api/test")

    def test_timeout_error_raises_api_error(self):
        """Test that timeout errors are wrapped in ApiError."""
        # Arrange
        mock_auth_manager = Mock(spec=AuthenticationManager)
        mock_auth_manager.get_auth_headers.return_value = {
            "Authorization": "Bearer test-token"
        }

        api_client = NetatmoApiClient(
            endpoint="https://api.netatmo.com",
            auth_manager=mock_auth_manager,
            timeout=1,
        )

        # Mock timeout
        with responses.RequestsMock() as rsps:
            rsps.get(
                "https://api.netatmo.com/api/test",
                body=requests.Timeout("Request timeout"),
            )

            # Act & Assert
            with pytest.raises(ApiError, match="timeout"):
                api_client.get("/api/test")
