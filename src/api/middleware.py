import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
)

from src.config.logging import get_logger


logger = get_logger(__name__)


class RequestContextMiddleware(
    BaseHTTPMiddleware
):
    """
    Middleware for request tracing.

    Adds:
    - request ID
    - latency measurement
    - structured request logs
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:

        request_id = str(uuid.uuid4())

        start_time = time.perf_counter()


        # Store request ID
        # for access inside routes/services
        request.state.request_id = request_id


        try:

            response = await call_next(
                request
            )


        except Exception:

            logger.exception(
                "Unhandled application error | request_id=%s",
                request_id,
            )

            raise


        finally:

            latency = (
                time.perf_counter()
                - start_time
            )

            logger.info(
                (
                    "%s %s | "
                    "request_id=%s | "
                    "latency_ms=%.2f"
                ),
                request.method,
                request.url.path,
                request_id,
                latency * 1000,
            )


        response.headers[
            "X-Request-ID"
        ] = request_id


        return response
