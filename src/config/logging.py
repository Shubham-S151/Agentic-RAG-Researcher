import logging
import sys
from typing import Optional

from src.config.settings import settings


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


def setup_logging() -> None:
    """
    Configure application-wide logging.

    This should be called once during application startup.
    """

    log_level = (
        logging.DEBUG
        if settings.debug
        else logging.INFO
    )

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(formatter)

    root_logger = logging.getLogger()

    root_logger.setLevel(log_level)

    # Prevent duplicate handlers when FastAPI reloads
    if not root_logger.handlers:
        root_logger.addHandler(handler)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Returns a module-specific logger.

    Example:

        logger = get_logger(__name__)

        logger.info("Retrieval started")
    """

    return logging.getLogger(
        name if name else "agentic-rag"
    )
