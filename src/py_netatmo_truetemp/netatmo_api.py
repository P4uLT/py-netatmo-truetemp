"""Netatmo API client facade interface."""

import logging
import os

import platformdirs
import requests

from .api_client import NetatmoApiClient
from .auth_manager import AuthenticationManager
from .cookie_store import CookieStore
from .home_service import HomeService
from .thermostat_service import ThermostatService
from .types import HomesDataResponse, HomeStatusResponse, TrueTemperatureResponse

logger = logging.getLogger(__name__)


class NetatmoAPI:
    """Main interface for Netatmo API operations.

    Example:
        >>> api = NetatmoAPI(
        ...     username=os.environ['NETATMO_USERNAME'],
        ...     password=os.environ['NETATMO_PASSWORD']
        ... )
        >>> homes = api.homesdata()
        >>> api.set_thermostat_mode(mode="schedule")
    """

    DEFAULT_ENDPOINT = "https://api.netatmo.com"

    def __init__(
        self,
        username: str,
        password: str,
        home_id: str | None = None,
        endpoint: str = DEFAULT_ENDPOINT,
        cookies_file: str | None = None,
        session: requests.Session | None = None,
    ) -> None:
        logger.info("Initializing Netatmo API client")

        self.endpoint = endpoint

        if cookies_file is None:
            cache_dir = platformdirs.user_cache_dir("netatmo", "py-netatmo-truetemp")
            os.makedirs(cache_dir, mode=0o700, exist_ok=True)
            cookies_file = os.path.join(cache_dir, "cookies.json")

        # Create shared session
        self._session = session or requests.Session()

        self._cookie_store = CookieStore(cookies_file)
        self._auth_manager = AuthenticationManager(
            username=username,
            password=password,
            cookie_store=self._cookie_store,
            session=self._session,
        )
        self._api_client = NetatmoApiClient(
            endpoint=self.endpoint,
            auth_manager=self._auth_manager,
            session=self._session,
        )
        self._home_service = HomeService(api_client=self._api_client)
        self._thermostat_service = ThermostatService(
            api_client=self._api_client, home_service=self._home_service
        )

        # Set default home if provided
        if home_id is not None:
            self._home_service.set_default_home_id(home_id)

    def homesdata(
        self, home_id: str | None = None, gateways_types: list[str] | None = None
    ) -> HomesDataResponse:
        """Returns homes data from Netatmo API."""
        return self._home_service.get_homes_data(
            home_id=home_id, gateways_types=gateways_types
        )

    def homestatus(
        self, home_id: str | None = None, device_types: list[str] | None = None
    ) -> HomeStatusResponse:
        """Returns current status of a home."""
        return self._home_service.get_home_status(
            home_id=home_id, device_types=device_types
        )

    def get_default_home_id(self) -> str:
        """Returns the default home ID."""
        return self._home_service.get_default_home_id()

    def list_thermostat_rooms(self, home_id: str | None = None) -> list[dict[str, str]]:
        """Lists all rooms with thermostats in a home."""
        return self._thermostat_service.list_rooms_with_thermostats(home_id=home_id)

    def set_truetemperature(
        self,
        room_id: str,
        corrected_temperature: float,
        home_id: str | None = None,
    ) -> TrueTemperatureResponse:
        """Sets calibrated temperature for a room."""
        return self._thermostat_service.set_room_temperature(
            room_id=room_id,
            corrected_temperature=corrected_temperature,
            home_id=home_id,
        )

    def __enter__(self) -> "NetatmoAPI":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._session.close()
