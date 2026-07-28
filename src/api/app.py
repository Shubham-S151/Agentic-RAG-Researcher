from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.middleware import (
    RequestContextMiddleware,
)

from src.api.routes import router

from src.config.logging import get_logger
from src.config.settings import settings


logger = get_logger(__name__)


def create_api_app() -> FastAPI:
    """
    Creates and configures the FastAPI application.

    This function follows the application factory pattern,
    making testing and deployment easier.
    """

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Production Agentic RAG "
            "Research Assistant API"
        ),
    )


    # --------------------------------------------------
    # Middleware
    # --------------------------------------------------

    app.add_middleware(
        RequestContextMiddleware
    )


    # --------------------------------------------------
    # CORS
    # --------------------------------------------------

    app.add_middleware(
        CORSMiddleware,

        allow_origins=[
            "*"
        ],

        allow_credentials=True,

        allow_methods=[
            "*"
        ],

        allow_headers=[
            "*"
        ],
    )


    # --------------------------------------------------
    # Routes
    # --------------------------------------------------

    app.include_router(
        router
    )


    # --------------------------------------------------
    # Health Endpoint
    # --------------------------------------------------

    @app.get(
        "/health",
        tags=["System"],
    )
    async def health_check():
        """
        Basic service health check.

        Used by:
        - Docker
        - Kubernetes
        - Load balancers
        """

        return {
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.app_version,
        }


    @app.get(
        "/ready",
        tags=["System"],
    )
    async def readiness_check():
        """
        Readiness endpoint.

        Later this will verify:

        - Qdrant availability
        - LLM availability
        - Search provider status
        """

        return {
            "status": "ready"
        }


    logger.info(
        "FastAPI application configured"
    )


    return app
