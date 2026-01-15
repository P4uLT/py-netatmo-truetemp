"""Tests for AuthenticationManager."""

import responses

from py_netatmo_truetemp.auth_manager import AuthenticationManager
from py_netatmo_truetemp.cookie_store import CookieStore


class TestInitialAuthentication:
    """Tests for initial authentication flow."""

    @responses.activate
    def test_initial_authentication_success(self, tmp_path):
        """Test successful initial authentication with cookie storage."""
        # Arrange: Setup mock HTTP responses
        cookie_file = tmp_path / "cookies.json"
        mock_cookie_store = CookieStore(str(cookie_file))

        # Mock the complete authentication flow
        # Step 1: Get initial session
        responses.get(
            "https://auth.netatmo.com/en-us/access/login",
            status=200,
            headers={"Set-Cookie": "session=initial-session-123"},
        )

        # Step 2: Get CSRF token (called during authentication)
        responses.get(
            "https://auth.netatmo.com/access/csrf",
            json={"token": "csrf-token-123"},
            status=200,
        )

        # Step 3: Submit login credentials
        responses.post(
            "https://auth.netatmo.com/access/postlogin",
            status=302,
            headers={"Set-Cookie": "netatmocomaccess_token=test-access-token%7Cvalue"},
        )

        # Step 4: Complete authentication flow
        responses.get(
            "https://auth.netatmo.com/access/keychain",
            status=200,
        )

        # Act: Perform authentication
        auth_manager = AuthenticationManager(
            username="test@example.com",
            password="password",
            cookie_store=mock_cookie_store,
        )
        headers = auth_manager.get_auth_headers()

        # Assert: Verify authentication successful
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Bearer ")
        assert "User-Agent" in headers
        assert headers["User-Agent"] == "netatmo-home"

        # Verify cookies were saved to filesystem
        assert cookie_file.exists()

        # Verify cookie file has secure permissions (on Unix systems)
        import sys
        import stat

        if sys.platform != "win32":
            file_mode = cookie_file.stat().st_mode
            assert stat.S_IMODE(file_mode) == 0o600
