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


class TestHTTPStatusCodes:
    """Tests for HTTP status code handling."""

    @pytest.mark.parametrize(
        "status_code,error_message",
        [
            (404, "HTTP 404"),
            (500, "HTTP 500"),
            (502, "HTTP 502"),
            (503, "HTTP 503"),
        ],
    )
    @responses.activate
    def test_http_errors_raise_api_error(self, status_code, error_message):
        """Test that HTTP errors raise ApiError with status code."""
        # Arrange
        mock_auth_manager = Mock(spec=AuthenticationManager)
        mock_auth_manager.get_auth_headers.return_value = {
            "Authorization": "Bearer test-token"
        }

        api_client = NetatmoApiClient(
            endpoint="https://api.netatmo.com",
            auth_manager=mock_auth_manager,
        )

        responses.get(
            "https://api.netatmo.com/api/test",
            status=status_code,
            json={"error": "Server error"},
        )

        # Act & Assert
        with pytest.raises(ApiError, match=error_message) as exc_info:
            api_client.get("/api/test")

        assert exc_info.value.status_code == status_code

    @responses.activate
    def test_403_triggers_auth_retry(self):
        """Test that 403 errors trigger authentication retry."""
        # Arrange
        mock_auth_manager = Mock(spec=AuthenticationManager)
        mock_auth_manager.get_auth_headers.return_value = {
            "Authorization": "Bearer test-token"
        }

        api_client = NetatmoApiClient(
            endpoint="https://api.netatmo.com",
            auth_manager=mock_auth_manager,
        )

        # First call returns 403, second call succeeds
        responses.get(
            "https://api.netatmo.com/api/test",
            status=403,
            json={"error": "Forbidden"},
        )
        responses.get(
            "https://api.netatmo.com/api/test",
            status=200,
            json={"status": "ok"},
        )

        # Act
        result = api_client.get("/api/test")

        # Assert: Verify retry happened
        assert result["status"] == "ok"
        assert mock_auth_manager.invalidate.called
        assert mock_auth_manager.get_auth_headers.call_count == 2
