"""Persistent cookie storage with secure permissions."""

import json
import os

from .logger import setup_logger

logger = setup_logger(__name__)


class CookieStore:
    """Manages persistent cookie storage with secure file permissions."""

    def __init__(self, cookies_file: str):
        self.cookies_file = cookies_file

    def load(self) -> dict[str, str] | None:
        """Loads cookies from storage."""
        if not os.path.exists(self.cookies_file):
            logger.debug(f"Cookies file does not exist: {self.cookies_file}")
            return None

        try:
            with open(self.cookies_file, "r") as f:
                cookies = json.load(f)
            logger.debug(f"Loaded cookies from {self.cookies_file}")
            return cookies
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error loading cookies: {e}")
            self._remove_invalid_file()
            return None

    def save(self, cookies: dict[str, str]) -> None:
        """Saves cookies to storage with secure permissions."""
        temp_dir = os.path.dirname(self.cookies_file)
        if not os.path.exists(temp_dir):
            logger.info(f"Creating directory: {temp_dir}")
            os.makedirs(temp_dir, mode=0o700)  # Secure permissions

        try:
            with open(self.cookies_file, "w") as f:
                json.dump(cookies, f, indent=2)

            # Set secure file permissions (owner read/write only)
            os.chmod(self.cookies_file, 0o600)
            logger.info(f"Saved cookies to {self.cookies_file}")
        except (IOError, OSError) as e:
            logger.error(f"Error saving cookies: {e}")
            raise

    def clear(self) -> None:
        """Removes stored cookies."""
        self._remove_invalid_file()

    def _remove_invalid_file(self) -> None:
        if os.path.exists(self.cookies_file):
            try:
                os.remove(self.cookies_file)
                logger.info(f"Removed cookies file: {self.cookies_file}")
            except OSError as e:
                logger.error(f"Error removing cookies file: {e}")
