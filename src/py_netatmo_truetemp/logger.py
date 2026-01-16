"""Logging utilities for py_netatmo_truetemp package."""

import logging


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given module name.

    Args:
        name: The logger name (typically __name__ from the calling module)

    Returns:
        logging.Logger: Logger instance configured by the application

    Note:
        This library does not configure handlers. Applications using this
        library should configure logging via logging.basicConfig() or their
        own handler setup.
    """
    return logging.getLogger(name)
