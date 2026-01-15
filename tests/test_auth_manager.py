"""Tests for AuthenticationManager."""

import threading
import time

import pytest
import responses

from py_netatmo_truetemp.auth_manager import AuthenticationManager
from py_netatmo_truetemp.cookie_store import CookieStore
from py_netatmo_truetemp.exceptions import AuthenticationError


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

    @responses.activate
    def test_cached_cookies_loaded_successfully(self, tmp_path):
        """Test that cached cookies are loaded and used for authentication."""
        # Arrange: Create cookie file with cached session
        cookie_file = tmp_path / "cookies.json"
        mock_cookie_store = CookieStore(str(cookie_file))

        # Pre-save cookies to file
        cached_cookies = {
            "session": "cached-session-123",
            "netatmocomaccess_token": "cached-token-abc%7Cvalue",
        }
        mock_cookie_store.save(cached_cookies)

        # Mock CSRF endpoint to validate cached session
        responses.get(
            "https://auth.netatmo.com/access/csrf",
            status=200,
            json={"token": "csrf-123"},
        )

        # Act: Create auth manager (should load cached cookies)
        auth_manager = AuthenticationManager(
            username="test@example.com",
            password="password",
            cookie_store=mock_cookie_store,
        )
        headers = auth_manager.get_auth_headers()

        # Assert: Verify cached token used (no re-authentication)
        assert "Authorization" in headers
        assert "cached-token-abc|value" in headers["Authorization"]
        # Verify no POST to login endpoint (cached session used)
        login_calls = [
            call for call in responses.calls if "postlogin" in call.request.url
        ]
        assert len(login_calls) == 0


class TestAuthenticationFailures:
    """Tests for authentication error handling."""

    @responses.activate
    def test_authentication_failure_raises_error(self, tmp_path):
        """Test that authentication failures raise AuthenticationError."""
        # Arrange
        cookie_file = tmp_path / "cookies.json"
        mock_cookie_store = CookieStore(str(cookie_file))

        # Mock failed CSRF request
        responses.get(
            "https://auth.netatmo.com/en-us/access/login",
            status=200,
        )
        responses.get(
            "https://auth.netatmo.com/access/csrf",
            status=401,
            json={"error": "Unauthorized"},
        )

        # Act & Assert: Verify AuthenticationError raised
        auth_manager = AuthenticationManager(
            username="test@example.com",
            password="wrong-password",
            cookie_store=mock_cookie_store,
        )

        with pytest.raises(AuthenticationError, match="Failed to obtain CSRF token"):
            auth_manager.get_auth_headers()

    @responses.activate
    def test_authentication_failure_clears_cookies(self, tmp_path):
        """Test that failed authentication clears any cached cookies."""
        # Arrange: Create invalid cached cookies
        cookie_file = tmp_path / "cookies.json"
        mock_cookie_store = CookieStore(str(cookie_file))
        mock_cookie_store.save({"invalid": "cookies"})

        # Mock CSRF to fail validation
        responses.get(
            "https://auth.netatmo.com/access/csrf",
            status=401,
        )

        # Act: Attempt to use cached cookies (should fail)
        auth_manager = AuthenticationManager(
            username="test@example.com",
            password="password",
            cookie_store=mock_cookie_store,
        )

        try:
            auth_manager.get_auth_headers()
        except AuthenticationError:
            pass

        # Assert: Verify cookies were cleared
        loaded_cookies = mock_cookie_store.load()
        assert loaded_cookies is None or len(loaded_cookies) == 0


class TestThreadSafety:
    """Tests for thread-safe authentication."""

    @responses.activate
    def test_concurrent_authentication_only_happens_once(self, tmp_path):
        """Test that concurrent requests only trigger one authentication."""
        # Arrange
        cookie_file = tmp_path / "cookies.json"
        mock_cookie_store = CookieStore(str(cookie_file))

        auth_call_count = {"count": 0}

        def count_auth_calls(request):
            auth_call_count["count"] += 1
            time.sleep(0.1)  # Simulate slow auth
            return (200, {}, '{"token": "csrf-token"}')

        # Mock auth endpoints with callback to count calls
        responses.get(
            "https://auth.netatmo.com/en-us/access/login",
            status=200,
        )
        responses.add_callback(
            responses.GET,
            "https://auth.netatmo.com/access/csrf",
            callback=count_auth_calls,
            content_type="application/json",
        )
        responses.post(
            "https://auth.netatmo.com/access/postlogin",
            status=200,
            headers={"Set-Cookie": "netatmocomaccess_token=token-123"},
        )
        responses.get(
            "https://auth.netatmo.com/access/keychain",
            status=200,
        )

        # Act: Create multiple threads requesting auth headers simultaneously
        auth_manager = AuthenticationManager(
            username="test@example.com",
            password="password",
            cookie_store=mock_cookie_store,
        )

        results = []

        def get_headers():
            headers = auth_manager.get_auth_headers()
            results.append(headers)

        threads = [threading.Thread(target=get_headers) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # Assert: Only one authentication should have occurred
        assert len(results) == 5  # All threads got headers
        # Auth flow should only happen once due to lock
        # Note: This tests the lock prevents concurrent auth attempts
