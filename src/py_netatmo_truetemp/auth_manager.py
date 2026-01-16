"""Netatmo authentication and token management."""

import json
import threading
import time

import requests

from .constants import ApiEndpoints, CookieNames, HttpHeaders
from .cookie_store import CookieStore
from .exceptions import AuthenticationError
from .logger import get_logger

logger = get_logger(__name__)


class AuthenticationManager:
    """Handles Netatmo authentication with cookie-based session persistence."""

    def __init__(
        self,
        username: str,
        password: str,
        cookie_store: CookieStore,
        session: requests.Session | None = None,
    ):
        self.username = username
        self.password = password
        self.cookie_store = cookie_store
        self.session: requests.Session = session or requests.Session()
        self._token: str | None = None
        self._token_obtained_at: float | None = None
        self._token_lock = threading.Lock()
        self._session_lock = threading.Lock()

    def get_auth_headers(self) -> dict[str, str]:
        """Returns authentication headers with Bearer token.

        Raises:
            AuthenticationError: If unable to obtain authentication token
        """
        with self._token_lock:
            if self._token is None or self._is_token_expired():
                self._token = self._obtain_token()
                self._token_obtained_at = time.time()

        return {
            "User-Agent": HttpHeaders.USER_AGENT,
            "accept": HttpHeaders.ACCEPT_JSON,
            "Authorization": f"Bearer {self._token}",
        }

    def _is_token_expired(self) -> bool:
        """Checks if cached token is expired (2.5 hour threshold)."""
        if self._token_obtained_at is None:
            return True

        # Consider token expired after 2.5 hours (9000 seconds)
        max_token_age = 9000
        current_age = time.time() - self._token_obtained_at
        is_expired = current_age > max_token_age

        if is_expired:
            logger.info(
                f"Token expired (age: {current_age:.0f}s, max: {max_token_age}s)"
            )

        return is_expired

    def _obtain_token(self) -> str:
        """Obtains authentication token from session.

        Raises:
            AuthenticationError: If unable to obtain token
        """
        try:
            headers = self._get_session_headers()
            token = headers["Authorization"].split(" ")[1]
            return token
        except (KeyError, IndexError) as e:
            logger.error(f"Error extracting token from headers: {e}")
            raise AuthenticationError("Failed to extract authentication token") from e
        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error obtaining token: {e}")
            raise AuthenticationError(
                f"Failed to obtain authentication token: {e}"
            ) from e

    def _get_session_headers(self) -> dict[str, str]:
        """Returns authenticated session headers.

        Raises:
            AuthenticationError: If unable to obtain session token
        """
        # Try cached session first
        cached_headers = self._try_cached_session()
        if cached_headers:
            return cached_headers

        # Perform fresh authentication
        return self._perform_fresh_authentication()

    def _try_cached_session(self) -> dict[str, str] | None:
        """Attempts to use cached session cookies."""
        cookies = self.cookie_store.load()
        if not cookies:
            return None

        with self._session_lock:
            # Restore cookies to session
            for name, value in cookies.items():
                self.session.cookies.set(name, value, domain=".netatmo.com")

            # Validate session
            try:
                response = self.session.get(
                    f"{ApiEndpoints.AUTH_BASE}{ApiEndpoints.CSRF}"
                )
                if response.status_code != 200:
                    logger.info("Cached session is invalid")
                    self.cookie_store.clear()
                    return None

                headers = self._extract_headers_from_cookies()
                test_response = self.session.get(
                    f"{ApiEndpoints.AUTH_BASE}{ApiEndpoints.CSRF}", headers=headers
                )
                if test_response.status_code == 200:
                    logger.info("Using cached session credentials")
                    return headers
                else:
                    self.cookie_store.clear()
                    return None

            except requests.exceptions.RequestException as e:
                logger.warning(f"Network error validating cached session: {e}")
                self.cookie_store.clear()
                return None
            except Exception as e:
                logger.warning(f"Error validating cached session: {e}")
                self.cookie_store.clear()
                return None

    def _perform_fresh_authentication(self) -> dict[str, str]:
        """Performs fresh authentication flow.

        Raises:
            AuthenticationError: If authentication fails
        """
        logger.info("Performing fresh authentication")

        with self._session_lock:
            try:
                # Step 1: Get initial session
                headers = {"User-Agent": HttpHeaders.USER_AGENT}
                response = self.session.get(
                    f"{ApiEndpoints.AUTH_BASE}{ApiEndpoints.LOGIN}", headers=headers
                )
                if response.status_code != 200:
                    raise AuthenticationError(
                        f"Login page request failed: {response.status_code}"
                    )

                logger.info("Got initial session cookie")

                # Step 2: Set required cookie
                self.session.cookies.set(
                    CookieNames.LAST_APP_USED, "app_thermostat", domain=".netatmo.com"
                )

                # Step 3: Get CSRF token
                csrf_response = self.session.get(
                    f"{ApiEndpoints.AUTH_BASE}{ApiEndpoints.CSRF}"
                )
                if csrf_response.status_code != 200:
                    raise AuthenticationError("Failed to obtain CSRF token")

                token_data = json.loads(csrf_response.text)
                csrf_token = token_data["token"]

                # Step 4: Submit login credentials
                payload = {
                    "email": self.username,
                    "password": self.password,
                    "stay_logged": "on",
                    "_token": csrf_token,
                }
                self.session.post(
                    f"{ApiEndpoints.AUTH_BASE}{ApiEndpoints.POST_LOGIN}",
                    data=payload,
                    headers=headers,
                )

                # Step 5: Complete authentication flow
                param = {"next_url": "https://my.netatmo.com"}
                self.session.get(
                    f"{ApiEndpoints.AUTH_BASE}{ApiEndpoints.KEYCHAIN}",
                    params=param,
                    headers=headers,
                )

                # Step 6: Extract access token
                auth_headers = self._extract_headers_from_cookies()
                logger.debug(f"Extracted headers: {list(auth_headers.keys())}")
                logger.debug(f"Session cookies: {list(self.session.cookies.keys())}")

                logger.info("Authentication successful")

                # Step 7: Save session cookies
                try:
                    self.cookie_store.save(self.session.cookies.get_dict())
                except (IOError, OSError) as e:
                    logger.warning(
                        f"Failed to cache session cookies: {e}. Will re-authenticate on next run."
                    )

                return auth_headers

            except AuthenticationError:
                raise
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error during authentication: {e}")
                raise AuthenticationError(
                    f"Network error during authentication: {e}"
                ) from e
            except (KeyError, json.JSONDecodeError) as e:
                logger.error(f"Error parsing authentication response: {e}")
                raise AuthenticationError(
                    f"Failed to parse authentication response: {e}"
                ) from e
            except Exception as e:
                logger.error(f"Unexpected error during authentication: {e}")
                raise AuthenticationError(f"Authentication failed: {e}") from e

    def _extract_headers_from_cookies(self) -> dict[str, str]:
        """Extracts access token from session cookies.

        Raises:
            AuthenticationError: If access token cookie not found
        """
        cookies = self.session.cookies.get_dict()
        if CookieNames.ACCESS_TOKEN not in cookies:
            raise AuthenticationError(
                f"Access token cookie not found: {CookieNames.ACCESS_TOKEN}"
            )

        access_token = cookies[CookieNames.ACCESS_TOKEN].replace("%7C", "|")

        return {
            "User-Agent": HttpHeaders.USER_AGENT,
            "Accept": HttpHeaders.ACCEPT_JSON,
            "Content-Type": HttpHeaders.CONTENT_TYPE_JSON,
            "Authorization": f"Bearer {access_token}",
        }

    def invalidate(self) -> None:
        """Invalidates current authentication and clears cached credentials."""
        with self._token_lock:
            self._token = None
            self._token_obtained_at = None
        with self._session_lock:
            self.session.cookies.clear()
        self.cookie_store.clear()
        logger.info("Authentication invalidated")
