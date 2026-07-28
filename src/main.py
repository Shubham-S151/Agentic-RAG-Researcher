from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.logging import get_logger, setup_logging
from src.config.settings import settings


logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle manager.

    Handles startup and shutdown events.

    Startup:
        - Initialize logging
        - Validate configuration
        - Initialize external services later

    Shutdown:
        - Close resources
        - Cleanup connections
    """

    # -------------------------
    # Startup
    # -------------------------

    setup_logging()

    logger.info(
        "Starting application: %s",
        settings.app_name,
    )

    logger.info(
        "Environment: %s",
        settings.environment,
    )


    # Future initialization points:
    #
    # await qdrant_client.connect()
    #
    # await embedding_service.load_model()
    #
    # await reranker.load_model()


    yield


    # -------------------------
    # Shutdown
    # -------------------------

    logger.info(
        "Shutting down application"
    )


def create_application() -> FastAPI:
    """
    Application factory.

    Using a factory instead of creating a global
    FastAPI instance improves testing and deployment.
    """

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Production-grade Agentic RAG "
            "Research Assistant API"
        ),
        lifespan=lifespan,
    )


    # Routes will be added here later:
    #
    # from src.api.routes import router
    #
    # application.include_router(router)


    return application


app = create_application()
