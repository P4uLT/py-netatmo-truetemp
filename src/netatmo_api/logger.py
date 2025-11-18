"""Logging configuration for netatmo_api package."""

import logging
import os


def setup_logger(name: str) -> logging.Logger:
    """Set up a logger with consistent formatting across the application.

    Args:
        name: The logger name (typically __name__ from the calling module)

    Returns:
        logging.Logger: Configured logger instance
    """
    environment = os.environ.get("ENVIRONMENT", "prod").lower()

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger

    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        f'%(levelname)-8s [%(filename)s:%(lineno)d] ({environment}) - %(message)s'
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False

    return logger
