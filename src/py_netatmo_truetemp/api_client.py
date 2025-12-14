"""HTTP client for Netatmo API with automatic authentication and retry."""

from typing import Any, Callable, TypeVar

import requests

from .auth_manager import AuthenticationManager
from .exceptions import ApiError
from .logger import setup_logger

logger = setup_logger(__name__)

# TypeVar for generic response types
T = TypeVar("T")


class NetatmoApiClient:
    """HTTP client for Netatmo API with automatic authentication retry."""

    def __init__(
        self,
        endpoint: str,
        auth_manager: AuthenticationManager,
        session: requests.Session | None = None,
        timeout: int = 30,
    ):
        self.endpoint = endpoint
        self.auth_manager = auth_manager
        self.session = session or requests.Session()
        self.timeout = timeout

    def _authenticated_request(
        self,
        method: Callable,
        url: str,
        path: str,
        max_retries: int = 1,
        **request_kwargs,
    ) -> dict[str, Any]:
        """Makes authenticated HTTP request with automatic retry on auth failures.

        Raises:
            ApiError: If the API request fails after retries
        """
        for attempt in range(max_retries + 1):
            try:
                headers = self.auth_manager.get_auth_headers()
                response = method(
                    url, headers=headers, timeout=self.timeout, **request_kwargs
                )
                response.raise_for_status()
                return response.json()

            except requests.exceptions.HTTPError as e:
                # Check if this is an authentication error (403) and we haven't exhausted retries
                if attempt < max_retries and self._is_authentication_error(e):
                    logger.warning(
                        f"Authentication failed for {path} (attempt {attempt + 1}), "
                        f"retrying with fresh authentication..."
                    )
                    self.auth_manager.invalidate()  # Force fresh authentication
                    continue  # Retry the request

                logger.error(f"GET {path} failed with status {e.response.status_code}")
                raise ApiError(
                    f"HTTP {e.response.status_code} for GET {path}",
                    e.response.status_code,
                ) from e
            except requests.exceptions.Timeout as e:
                logger.error(f"Timeout during {path}")
                raise ApiError(f"Request timeout for {path}") from e
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error during {path}: {e}")
                raise ApiError(f"Network error for {path}: {e}") from e

        raise ApiError(f"Request to {path} failed after {max_retries + 1} attempts")

    def _is_authentication_error(self, e: requests.exceptions.HTTPError) -> bool:
        """Checks if an HTTPError is due to authentication failure."""
        # Check for 403 Forbidden (token expired or invalid)
        # and look for "expired" in the response
        if e.response.status_code == 403:
            try:
                content = e.response.text.lower()
                if (
                    "expired" in content
                    or "invalid" in content
                    or "forbidden" in content
                ):
                    logger.warning(
                        f"Detected authentication error (403): {content[:200]}"
                    )
                    return True
            except Exception:
                # If we can't parse the response, assume it's auth-related
                return True
        return False

    def get(self, path: str, params: dict | None = None) -> dict[str, Any]:
        """Sends GET request to API.

        Raises:
            ApiError: If the API request fails
        """
        url = f"{self.endpoint}{path}"
        return self._authenticated_request(self.session.get, url, path, params=params)

    def get_typed(
        self, path: str, response_type: type[T], params: dict | None = None
    ) -> T:
        """Sends GET request to API and returns typed response.

        Args:
            path: API endpoint path
            response_type: The expected response type (e.g., HomesDataResponse)
            params: Query parameters

        Returns:
            Response data typed as T

        Raises:
            ApiError: If the API request fails
        """
        result = self.get(path, params)
        # The type checker will trust this cast since we're explicitly
        # declaring the return type through the response_type parameter
        return result  # type: ignore[return-value]

    def post(
        self, path: str, params: dict | None = None, json_data: dict | None = None
    ) -> dict[str, Any]:
        """Sends POST request to API.

        Raises:
            ApiError: If the API request fails
        """
        url = f"{self.endpoint}{path}"

        # Log request details before making the call
        logger.debug(f"POST {path}")
        logger.debug(f"  URL: {url}")
        if params:
            logger.debug(f"  Params: {params}")
        if json_data:
            logger.debug(f"  JSON data: {json_data}")

        response = self._authenticated_request(
            self.session.post, url, path, params=params, json=json_data
        )

        logger.debug(f"  POST {path} response received")
        return response

    def post_typed(
        self,
        path: str,
        response_type: type[T],
        params: dict | None = None,
        json_data: dict | None = None,
    ) -> T:
        """Sends POST request to API and returns typed response.

        Args:
            path: API endpoint path
            response_type: The expected response type (e.g., TrueTemperatureResponse)
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data typed as T

        Raises:
            ApiError: If the API request fails
        """
        result = self.post(path, params, json_data)
        # The type checker will trust this cast since we're explicitly
        # declaring the return type through the response_type parameter
        return result  # type: ignore[return-value]
