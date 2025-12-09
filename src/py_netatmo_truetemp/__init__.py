"""Netatmo API client package.

Example:
    >>> from py_netatmo_truetemp import NetatmoAPI
    >>> api = NetatmoAPI(
    ...     username=os.environ['NETATMO_USERNAME'],
    ...     password=os.environ['NETATMO_PASSWORD']
    ... )
    >>> api.set_truetemperature(room_id="123", corrected_temperature=20.5)
"""

from .netatmo_api import NetatmoAPI
from .auth_manager import AuthenticationManager
from .cookie_store import CookieStore
from .api_client import NetatmoApiClient
from .home_service import HomeService
from .thermostat_service import ThermostatService
from .exceptions import (
    NetatmoError,
    AuthenticationError,
    ApiError,
    ValidationError,
    RoomNotFoundError,
    HomeNotFoundError,
)

__all__ = [
    "NetatmoAPI",
    "AuthenticationManager",
    "CookieStore",
    "NetatmoApiClient",
    "HomeService",
    "ThermostatService",
    "NetatmoError",
    "AuthenticationError",
    "ApiError",
    "ValidationError",
    "RoomNotFoundError",
    "HomeNotFoundError",
]
