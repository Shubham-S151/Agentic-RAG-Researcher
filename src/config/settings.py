from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration.

    Values are loaded from environment variables or a .env file.
    Every module in the application should import the singleton
    `settings` object instead of calling os.getenv().
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    app_name: str = Field(
        default="Agentic-RAG-Researcher",
        alias="APP_NAME",
    )

    app_version: str = Field(
        default="1.0.0",
        alias="APP_VERSION",
    )

    environment: Literal[
        "development",
        "testing",
        "production",
    ] = Field(
        default="development",
        alias="ENVIRONMENT",
    )

    debug: bool = Field(
        default=True,
        alias="DEBUG",
    )

    # ------------------------------------------------------------------
    # OpenAI
    # ------------------------------------------------------------------

    openai_api_key: str = Field(
        default="",
        alias="OPENAI_API_KEY",
    )

    generation_model: str = Field(
        default="gpt-4.1",
        alias="GENERATION_MODEL",
    )

    router_model: str = Field(
        default="gpt-4.1-mini",
        alias="ROUTER_MODEL",
    )

    # ------------------------------------------------------------------
    # Embeddings
    # ------------------------------------------------------------------

    embedding_model: str = Field(
        default="text-embedding-3-large",
        alias="EMBEDDING_MODEL",
    )

    embedding_dimension: int = Field(
        default=3072,
        alias="EMBEDDING_DIMENSION",
    )

    # ------------------------------------------------------------------
    # Qdrant
    # ------------------------------------------------------------------

    qdrant_url: str = Field(
        default="http://localhost:6333",
        alias="QDRANT_URL",
    )

    qdrant_api_key: str = Field(
        default="",
        alias="QDRANT_API_KEY",
    )

    qdrant_collection: str = Field(
        default="research_papers",
        alias="QDRANT_COLLECTION",
    )

    # ------------------------------------------------------------------
    # Tavily
    # ------------------------------------------------------------------

    tavily_api_key: str = Field(
        default="",
        alias="TAVILY_API_KEY",
    )

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    top_k_retrieval: int = Field(
        default=20,
        alias="TOP_K_RETRIEVAL",
    )

    top_k_rerank: int = Field(
        default=5,
        alias="TOP_K_RERANK",
    )

    # ------------------------------------------------------------------
    # FastAPI
    # ------------------------------------------------------------------

    host: str = Field(
        default="0.0.0.0",
        alias="HOST",
    )

    port: int = Field(
        default=8000,
        alias="PORT",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    Using lru_cache prevents repeatedly parsing the .env file
    and ensures a single shared configuration object.
    """
    return Settings()


settings = get_settings()
