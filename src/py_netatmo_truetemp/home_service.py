"""Home operations and status management."""

from typing import Any

from .api_client import NetatmoApiClient
from .constants import ApiEndpoints
from .exceptions import HomeNotFoundError
from .logger import setup_logger
from .types import HomesDataResponse, HomeStatusResponse
from .validators import validate_home_id

logger = setup_logger(__name__)


class HomeService:
    """Provides home-related operations and data retrieval."""

    def __init__(self, api_client: NetatmoApiClient):
        self.api_client = api_client
        self._default_home_id: str | None = None

    def get_homes_data(
        self, home_id: str | None = None, gateways_types: list[str] | None = None
    ) -> HomesDataResponse:
        """Returns homes data from Netatmo API.

        Raises:
            ValidationError: If home_id is invalid
            ApiError: If the API request fails
        """
        if home_id is not None:
            validate_home_id(home_id)

        parameters: dict[str, Any] = {}
        if home_id is not None:
            parameters["home_id"] = home_id
        if gateways_types is not None:
            parameters["gateways_types"] = gateways_types

        return self.api_client.get(ApiEndpoints.HOMES_DATA, params=parameters)

    def get_home_status(
        self, home_id: str | None = None, device_types: list[str] | None = None
    ) -> HomeStatusResponse:
        """Returns current status of a home.

        Raises:
            ValidationError: If home_id is invalid
            HomeNotFoundError: If no homes found
            ApiError: If the API request fails
        """
        if home_id is not None:
            validate_home_id(home_id)

        parameters: dict[str, Any] = {}
        if home_id is not None:
            parameters["home_id"] = home_id
        elif self._default_home_id is not None:
            parameters["home_id"] = self._default_home_id
        else:
            parameters["home_id"] = self.get_default_home_id()

        if device_types is not None:
            parameters["device_types"] = device_types

        return self.api_client.get(ApiEndpoints.HOME_STATUS, params=parameters)

    def get_default_home_id(self) -> str:
        """Returns the default home ID.

        Raises:
            HomeNotFoundError: If no homes found in response
            ApiError: If the API request fails
        """
        if self._default_home_id is not None:
            return self._default_home_id

        try:
            payload = self.get_homes_data()
            home_id = payload["body"]["homes"][0]["id"]
            self._default_home_id = home_id
            return home_id
        except (KeyError, IndexError) as e:
            logger.error(f"No homes found in account: {e}")
            raise HomeNotFoundError() from e

    def set_default_home_id(self, home_id: str) -> None:
        """Sets the default home ID for operations.

        Raises:
            ValidationError: If home_id is invalid
        """
        validate_home_id(home_id)
        self._default_home_id = home_id
