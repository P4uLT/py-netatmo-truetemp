"""Type definitions for Netatmo API responses."""

from typing import TypedDict, NotRequired, Literal


ResponseStatus = Literal["ok", "failed"]


class RoomStatus(TypedDict):
    """Room status from homestatus API."""

    id: str
    reachable: NotRequired[bool]
    therm_measured_temperature: NotRequired[float]
    therm_setpoint_temperature: NotRequired[float]
    therm_setpoint_mode: NotRequired[str]
    therm_setpoint_end_time: NotRequired[int]
    heating_power_request: NotRequired[int]
    anticipating: NotRequired[bool]
    open_window: NotRequired[bool]


class HomeStatus(TypedDict):
    """Home status data."""

    id: str
    rooms: list[RoomStatus]
    modules: NotRequired[list[dict]]


class HomeStatusBody(TypedDict):
    """Body of homestatus response."""

    home: HomeStatus


class HomeStatusResponse(TypedDict):
    """Response from /api/homestatus endpoint."""

    status: ResponseStatus
    time_server: int
    body: HomeStatusBody


class RoomInfo(TypedDict):
    """Room information from homesdata API."""

    id: str
    name: str
    type: NotRequired[str]
    module_ids: NotRequired[list[str]]


class ModuleInfo(TypedDict):
    """Module information."""

    id: str
    type: str
    name: str
    setup_date: NotRequired[int]
    room_id: NotRequired[str]


class HomeData(TypedDict):
    """Home data from homesdata API."""

    id: str
    name: str
    altitude: NotRequired[int]
    coordinates: NotRequired[list[float]]
    country: NotRequired[str]
    timezone: NotRequired[str]
    rooms: list[RoomInfo]
    modules: NotRequired[list[ModuleInfo]]
    therm_schedules: NotRequired[list[dict]]
    therm_setpoint_default_duration: NotRequired[int]


class HomesDataBody(TypedDict):
    """Body of homesdata response."""

    homes: list[HomeData]
    user: NotRequired[dict]


class HomesDataResponse(TypedDict):
    """Response from /api/homesdata endpoint."""

    status: ResponseStatus
    time_server: int
    body: HomesDataBody


class TrueTemperatureResponse(TypedDict):
    """Response from /api/truetemperature endpoint."""

    status: ResponseStatus
    time_server: int
