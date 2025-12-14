"""Custom exceptions for Netatmo API."""


class NetatmoError(Exception):
    """Base exception for all Netatmo-related errors."""

    pass


class AuthenticationError(NetatmoError):
    """Raised when authentication fails."""

    pass


class ApiError(NetatmoError):
    """Raised when API requests fail."""

    def __init__(self, message: str, status_code: int | None = None):
        """Initialize API error.

        Args:
            message: Error message
            status_code: HTTP status code if available
        """
        super().__init__(message)
        self.status_code = status_code


class ValidationError(NetatmoError):
    """Raised when input validation fails."""

    pass


class RoomNotFoundError(NetatmoError):
    """Raised when a room cannot be found."""

    def __init__(self, room_id: str):
        """Initialize room not found error.

        Args:
            room_id: The room ID that was not found
        """
        super().__init__(f"Room {room_id} not found")
        self.room_id = room_id


class HomeNotFoundError(NetatmoError):
    """Raised when a home cannot be found."""

    def __init__(self, home_id: str | None = None):
        """Initialize home not found error.

        Args:
            home_id: The home ID that was not found
        """
        message = f"Home {home_id} not found" if home_id else "No homes found"
        super().__init__(message)
        self.home_id = home_id
