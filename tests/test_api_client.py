"""Tests for NetatmoApiClient."""

import responses
import pytest
import requests
from unittest.mock import Mock

from py_netatmo_truetemp.api_client import NetatmoApiClient
from py_netatmo_truetemp.auth_manager import AuthenticationManager
from py_netatmo_truetemp.exceptions import ApiError


# ============================================================================
# Shared Fixtures
# ============================================================================


@pytest.fixture
def real_session() -> requests.Session:
    """Provide a real requests.Session for testing."""
    return requests.Session()


@pytest.fixture
def mock_auth_manager() -> Mock:
    """Provide a mocked AuthenticationManager."""
    mock = Mock(spec=AuthenticationManager)
    mock.get_auth_headers.return_value = {"Authorization": "Bearer test-token"}
    return mock


@pytest.fixture
def api_client(
    real_session: requests.Session, mock_auth_manager: Mock
) -> NetatmoApiClient:
    """Provide a NetatmoApiClient with real session and mock auth manager."""
    return NetatmoApiClient(
        endpoint="https://api.netatmo.com",
        auth_manager=mock_auth_manager,
        session=real_session,
    )


# ============================================================================
# Test Classes
# ============================================================================


class TestNetworkErrors:
    """Tests for network error handling."""

    @responses.activate
    def test_connection_error_raises_api_error(self, api_client: NetatmoApiClient):
        """Test that connection errors are wrapped in ApiError."""
        # Mock connection error
        responses.get(
            "https://api.netatmo.com/api/test",
            body=requests.ConnectionError("Connection refused"),
        )

        # Act & Assert
        with pytest.raises(ApiError, match="Network error"):
            api_client.get("/api/test")

    @responses.activate
    def test_timeout_error_raises_api_error(
        self, real_session: requests.Session, mock_auth_manager: Mock
    ):
        """Test that timeout errors are wrapped in ApiError."""
        # Create client with custom timeout
        api_client = NetatmoApiClient(
            endpoint="https://api.netatmo.com",
            auth_manager=mock_auth_manager,
            session=real_session,
            timeout=1,
        )

        # Mock timeout
        responses.get(
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
    def test_http_errors_raise_api_error(
        self, api_client: NetatmoApiClient, status_code, error_message
    ):
        """Test that HTTP errors raise ApiError with status code."""
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
    def test_403_triggers_auth_retry(
        self, api_client: NetatmoApiClient, mock_auth_manager: Mock
    ):
        """Test that 403 errors trigger authentication retry."""
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


# ============================================================================
# New Comprehensive Test Classes
# ============================================================================


class TestHTTPMechanics:
    """Test HTTP request construction and parameter handling."""

    @responses.activate
    def test_get_with_query_params(self, api_client: NetatmoApiClient):
        """Test GET request passes query parameters correctly."""
        responses.get(
            "https://api.netatmo.com/api/homesdata",
            match=[
                responses.matchers.query_param_matcher({"home_id": "home-123"}),
                responses.matchers.header_matcher(
                    {"Authorization": "Bearer test-token"}
                ),
            ],
            json={"status": "ok", "body": {}},
        )

        result = api_client.get("/api/homesdata", params={"home_id": "home-123"})

        assert result["status"] == "ok"
        assert len(responses.calls) == 1
        assert "home_id=home-123" in responses.calls[0].request.url

    @responses.activate
    def test_get_without_params(self, api_client: NetatmoApiClient):
        """Test GET request without parameters."""
        responses.get(
            "https://api.netatmo.com/api/test",
            json={"status": "ok"},
        )

        result = api_client.get("/api/test")

        assert result["status"] == "ok"
        assert len(responses.calls) == 1

    @responses.activate
    def test_post_with_json_data(self, api_client: NetatmoApiClient):
        """Test POST request with JSON body."""
        responses.post(
            "https://api.netatmo.com/api/truetemperature",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "room_id": "room-123",
                        "corrected_temperature": 21.5,
                    }
                ),
            ],
            json={"status": "ok"},
        )

        result = api_client.post(
            "/api/truetemperature",
            json_data={"room_id": "room-123", "corrected_temperature": 21.5},
        )

        assert result["status"] == "ok"
        assert len(responses.calls) == 1

    @responses.activate
    def test_post_with_params_only(self, api_client: NetatmoApiClient):
        """Test POST request with query parameters."""
        responses.post(
            "https://api.netatmo.com/api/endpoint",
            match=[
                responses.matchers.query_param_matcher({"home_id": "home-123"}),
            ],
            json={"status": "ok"},
        )

        result = api_client.post("/api/endpoint", params={"home_id": "home-123"})

        assert result["status"] == "ok"
        assert "home_id=home-123" in responses.calls[0].request.url

    @responses.activate
    def test_post_with_params_and_json(self, api_client: NetatmoApiClient):
        """Test POST request with both query params and JSON body."""
        responses.post(
            "https://api.netatmo.com/api/endpoint",
            match=[
                responses.matchers.query_param_matcher({"home_id": "home-123"}),
                responses.matchers.json_params_matcher({"data": "value"}),
            ],
            json={"status": "ok"},
        )

        result = api_client.post(
            "/api/endpoint",
            params={"home_id": "home-123"},
            json_data={"data": "value"},
        )

        assert result["status"] == "ok"
        assert "home_id=home-123" in responses.calls[0].request.url

    @responses.activate
    def test_get_typed_returns_correct_structure(self, api_client: NetatmoApiClient):
        """Test that get_typed returns correctly structured response."""
        from py_netatmo_truetemp.types import HomesDataResponse

        responses.get(
            "https://api.netatmo.com/api/homesdata",
            json={
                "status": "ok",
                "body": {"homes": [{"id": "home-123", "name": "My Home"}]},
            },
        )

        result = api_client.get_typed("/api/homesdata", HomesDataResponse)

        assert result["status"] == "ok"
        assert "body" in result
        assert "homes" in result["body"]

    @responses.activate
    def test_post_typed_with_all_parameters(self, api_client: NetatmoApiClient):
        """Test post_typed passes all parameters correctly."""
        from py_netatmo_truetemp.types import TrueTemperatureResponse

        responses.post(
            "https://api.netatmo.com/api/truetemperature",
            match=[
                responses.matchers.query_param_matcher({"home_id": "home-123"}),
                responses.matchers.json_params_matcher(
                    {"room_id": "room-123", "temp": 21.0}
                ),
            ],
            json={"status": "ok"},
        )

        result = api_client.post_typed(
            "/api/truetemperature",
            TrueTemperatureResponse,
            params={"home_id": "home-123"},
            json_data={"room_id": "room-123", "temp": 21.0},
        )

        assert result["status"] == "ok"

    @responses.activate
    def test_session_reuse_across_requests(
        self, real_session: requests.Session, mock_auth_manager: Mock
    ):
        """Test that multiple requests reuse the same session object."""
        api_client = NetatmoApiClient(
            endpoint="https://api.netatmo.com",
            auth_manager=mock_auth_manager,
            session=real_session,
        )

        # Mock multiple endpoints
        responses.get("https://api.netatmo.com/api/test1", json={"status": "ok"})
        responses.get("https://api.netatmo.com/api/test2", json={"status": "ok"})
        responses.post("https://api.netatmo.com/api/test3", json={"status": "ok"})

        # Make multiple calls
        api_client.get("/api/test1")
        api_client.get("/api/test2")
        api_client.post("/api/test3")

        # Verify same session was used (session ID should be same)
        assert api_client.session is real_session
        assert len(responses.calls) == 3


class TestRetryLogic:
    """Test authentication retry behavior."""

    @responses.activate
    def test_403_retry_exhaustion_raises_api_error(
        self, api_client: NetatmoApiClient, mock_auth_manager: Mock
    ):
        """Test that 403 errors exhaust retries and raise ApiError."""
        # Both attempts return 403 with auth error
        responses.get(
            "https://api.netatmo.com/api/test",
            status=403,
            json={"error": {"message": "Access token expired"}},
        )
        responses.get(
            "https://api.netatmo.com/api/test",
            status=403,
            json={"error": {"message": "Access token expired"}},
        )

        # Act & Assert
        with pytest.raises(ApiError, match="HTTP 403") as exc_info:
            api_client.get("/api/test")

        # Verify retry behavior
        assert exc_info.value.status_code == 403
        assert mock_auth_manager.invalidate.call_count == 1  # Only once
        assert mock_auth_manager.get_auth_headers.call_count == 2  # Initial + 1 retry
        assert len(responses.calls) == 2

    @responses.activate
    def test_403_with_empty_body_no_retry(
        self, api_client: NetatmoApiClient, mock_auth_manager: Mock
    ):
        """Test that 403 with empty body doesn't retry (server error)."""
        responses.get(
            "https://api.netatmo.com/api/test",
            status=403,
            body="",
        )

        # Act & Assert
        with pytest.raises(ApiError, match="HTTP 403"):
            api_client.get("/api/test")

        # Should NOT retry - empty body indicates server error
        assert mock_auth_manager.invalidate.call_count == 0
        assert mock_auth_manager.get_auth_headers.call_count == 1
        assert len(responses.calls) == 1

    @responses.activate
    def test_non_403_error_no_retry(
        self, api_client: NetatmoApiClient, mock_auth_manager: Mock
    ):
        """Test that non-403 errors don't trigger retry."""
        responses.get(
            "https://api.netatmo.com/api/test",
            status=500,
            json={"error": "Internal server error"},
        )

        # Act & Assert
        with pytest.raises(ApiError, match="HTTP 500"):
            api_client.get("/api/test")

        # Should not retry
        assert mock_auth_manager.invalidate.call_count == 0
        assert mock_auth_manager.get_auth_headers.call_count == 1
        assert len(responses.calls) == 1

    @responses.activate
    def test_retry_success_on_second_attempt(
        self, api_client: NetatmoApiClient, mock_auth_manager: Mock
    ):
        """Test successful retry after auth failure."""
        # First call returns 403, second succeeds
        responses.get(
            "https://api.netatmo.com/api/test",
            status=403,
            json={"error": "token expired"},
        )
        responses.get(
            "https://api.netatmo.com/api/test",
            status=200,
            json={"status": "ok", "data": "success"},
        )

        # Act
        result = api_client.get("/api/test")

        # Assert
        assert result["status"] == "ok"
        assert result["data"] == "success"
        assert mock_auth_manager.invalidate.call_count == 1
        assert mock_auth_manager.get_auth_headers.call_count == 2
        assert len(responses.calls) == 2

    @responses.activate
    def test_timeout_during_retry_attempt(
        self, api_client: NetatmoApiClient, mock_auth_manager: Mock
    ):
        """Test that timeout on retry attempt is handled."""
        # First call returns 403, second call times out
        responses.get(
            "https://api.netatmo.com/api/test",
            status=403,
            json={"error": "token expired"},
        )
        responses.get(
            "https://api.netatmo.com/api/test",
            body=requests.Timeout("Request timeout"),
        )

        # Act & Assert
        with pytest.raises(ApiError, match="timeout"):
            api_client.get("/api/test")

        # Verify retry was attempted
        assert mock_auth_manager.invalidate.call_count == 1
        assert len(responses.calls) == 2


class TestAuthenticationErrorDetection:
    """Test _is_authentication_error logic with various scenarios."""

    @pytest.mark.parametrize(
        "status_code,response_body,should_retry",
        [
            # 403s with any content - retry conservatively
            (403, '{"error": "token expired"}', True),
            (403, '{"error": "Forbidden"}', True),
            (
                403,
                '{"error": "rate limit"}',
                True,
            ),  # Conservative: retry even if might be rate limit
            (403, '{"error": "something unusual"}', True),
            (403, "not json", True),
            (403, "any text content", True),
            # Empty 403 responses - don't retry (server error)
            (403, "", False),
            (403, "   ", False),
            (403, "\n\t", False),
            # Non-403 status codes - never retry
            (401, '{"error": "unauthorized"}', False),
            (404, '{"error": "not found"}', False),
            (500, '{"error": "server error"}', False),
        ],
    )
    @responses.activate
    def test_is_authentication_error_detection(
        self,
        api_client: NetatmoApiClient,
        mock_auth_manager: Mock,
        status_code,
        response_body,
        should_retry,
    ):
        """Test _is_authentication_error with various response scenarios."""
        # Mock the HTTP call
        responses.get(
            "https://api.netatmo.com/api/test",
            status=status_code,
            body=response_body,
        )

        # Add success response for potential retry
        if should_retry and status_code == 403:
            responses.get(
                "https://api.netatmo.com/api/test",
                status=200,
                json={"status": "ok"},
            )

        # Act
        if should_retry and status_code == 403:
            # Should retry and succeed
            result = api_client.get("/api/test")
            assert result["status"] == "ok"
            assert mock_auth_manager.invalidate.call_count == 1
            assert len(responses.calls) == 2
        else:
            # Should fail immediately
            with pytest.raises(ApiError):
                api_client.get("/api/test")

            # For 403 non-auth errors, invalidate should NOT be called
            if status_code == 403 and not should_retry:
                assert mock_auth_manager.invalidate.call_count == 0
            assert len(responses.calls) == 1


class TestEdgeCases:
    """Test edge cases and error handling."""

    @responses.activate
    def test_malformed_json_response(self, api_client: NetatmoApiClient):
        """Test handling of malformed JSON response."""
        responses.get(
            "https://api.netatmo.com/api/test",
            status=200,
            body="not valid json{",
            content_type="application/json",
        )

        # Act & Assert
        with pytest.raises(ApiError, match="Network error"):
            api_client.get("/api/test")

    @responses.activate
    def test_empty_response_body(self, api_client: NetatmoApiClient):
        """Test handling of empty response body."""
        responses.get(
            "https://api.netatmo.com/api/test",
            status=200,
            body="",
        )

        # Act & Assert
        with pytest.raises(ApiError, match="Network error"):
            api_client.get("/api/test")

    @responses.activate
    def test_custom_timeout_configuration(
        self, real_session: requests.Session, mock_auth_manager: Mock
    ):
        """Test that custom timeout is used in requests."""
        api_client = NetatmoApiClient(
            endpoint="https://api.netatmo.com",
            auth_manager=mock_auth_manager,
            session=real_session,
            timeout=5,
        )

        responses.get(
            "https://api.netatmo.com/api/test",
            json={"status": "ok"},
        )

        result = api_client.get("/api/test")

        assert result["status"] == "ok"
        assert api_client.timeout == 5

    @responses.activate
    def test_auth_headers_included_in_requests(
        self, api_client: NetatmoApiClient, mock_auth_manager: Mock
    ):
        """Test that authentication headers are included in all requests."""
        responses.get(
            "https://api.netatmo.com/api/test",
            match=[
                responses.matchers.header_matcher(
                    {"Authorization": "Bearer test-token"}
                ),
            ],
            json={"status": "ok"},
        )

        result = api_client.get("/api/test")

        assert result["status"] == "ok"
        assert mock_auth_manager.get_auth_headers.called

    @responses.activate
    def test_session_injection_works(
        self, real_session: requests.Session, mock_auth_manager: Mock
    ):
        """Test that custom session can be injected."""
        custom_session = requests.Session()
        custom_session.headers.update({"X-Custom-Header": "test-value"})

        api_client = NetatmoApiClient(
            endpoint="https://api.netatmo.com",
            auth_manager=mock_auth_manager,
            session=custom_session,
        )

        responses.get(
            "https://api.netatmo.com/api/test",
            json={"status": "ok"},
        )

        result = api_client.get("/api/test")

        assert result["status"] == "ok"
        assert api_client.session is custom_session

    def test_403_with_corrupted_response_retries(
        self, api_client: NetatmoApiClient, mock_auth_manager: Mock
    ):
        """Test that corrupted 403 responses (AttributeError/TypeError) trigger retry."""
        # Create a mock HTTPError with broken response.text property
        mock_response = Mock()
        mock_response.status_code = 403
        # Simulate corrupted Response object where .text raises AttributeError
        mock_response.text = Mock(
            side_effect=AttributeError("text property unavailable")
        )

        http_error = requests.exceptions.HTTPError()
        http_error.response = mock_response

        # Act - should return True (retry) conservatively
        should_retry = api_client._is_authentication_error(http_error)

        # Assert
        assert should_retry is True
