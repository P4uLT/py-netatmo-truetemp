"""Constants for Netatmo API."""


class ApiEndpoints:
    """Netatmo API endpoints."""
    # Base URLs
    AUTH_BASE = "https://auth.netatmo.com"

    # API paths
    HOMES_DATA = "/api/homesdata"
    HOME_STATUS = "/api/homestatus"
    TRUE_TEMPERATURE = "/api/truetemperature"

    # Auth paths
    LOGIN = "/en-us/access/login"
    CSRF = "/access/csrf"
    POST_LOGIN = "/access/postlogin"
    KEYCHAIN = "/access/keychain"


class CookieNames:
    """Cookie names used for authentication."""

    ACCESS_TOKEN = "netatmocomaccess_token"
    LAST_APP_USED = "netatmocomlast_app_used"


class HttpHeaders:
    """HTTP header constants."""

    USER_AGENT = "netatmo-home"
    ACCEPT_JSON = "application/json"
    CONTENT_TYPE_JSON = "application/json"


class TemperatureLimits:
    """Temperature validation limits."""

    MIN_CELSIUS = -50.0
    MAX_CELSIUS = 50.0
