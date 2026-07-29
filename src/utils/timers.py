import time

from functools import wraps
from contextlib import contextmanager, asynccontextmanager

from src.config.logging import get_logger


logger = get_logger(__name__)


class Timer:
    """
    Simple reusable timer.

    Example:

        timer = Timer()

        timer.start()

        ...

        elapsed = timer.stop()
    """

    def __init__(self):

        self._start = None

    def start(self):

        self._start = time.perf_counter()

    def stop(self) -> float:

        if self._start is None:

            raise RuntimeError(
                "Timer has not been started."
            )

        elapsed = (
            time.perf_counter()
            - self._start
        )

        self._start = None

        return elapsed


@contextmanager
def timed(operation: str):
    """
    Context manager for synchronous timing.

    Example:

        with timed("Indexing"):
            ...
    """

    start = time.perf_counter()

    try:

        yield

    finally:

        elapsed = (
            time.perf_counter()
            - start
        )

        logger.info(
            "%s completed in %.3f seconds",
            operation,
            elapsed,
        )


@asynccontextmanager
async def async_timed(operation: str):
    """
    Context manager for asynchronous timing.

    Example:

        async with async_timed(
            "Retrieval"
        ):
            await retriever.retrieve(...)
    """

    start = time.perf_counter()

    try:

        yield

    finally:

        elapsed = (
            time.perf_counter()
            - start
        )

        logger.info(
            "%s completed in %.3f seconds",
            operation,
            elapsed,
        )


def measure_time(operation: str):
    """
    Decorator for timing synchronous functions.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            start = time.perf_counter()

            result = func(
                *args,
                **kwargs,
            )

            elapsed = (
                time.perf_counter()
                - start
            )

            logger.info(
                "%s completed in %.3f seconds",
                operation,
                elapsed,
            )

            return result

        return wrapper

    return decorator


def measure_async_time(operation: str):
    """
    Decorator for timing asynchronous functions.
    """

    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):

            start = time.perf_counter()

            result = await func(
                *args,
                **kwargs,
            )

            elapsed = (
                time.perf_counter()
                - start
            )

            logger.info(
                "%s completed in %.3f seconds",
                operation,
                elapsed,
            )

            return result

        return wrapper

    return decorator
