from functools import lru_cache

from src.config.logging import get_logger
from src.config.settings import settings


logger = get_logger(__name__)


# ============================================================
# LLM Dependency
# ============================================================


@lru_cache(maxsize=1)
def get_llm_client():
    """
    Creates and caches the LLM client.

    A single client instance is reused across requests.

    This avoids:
    - repeated authentication setup
    - unnecessary connections
    """

    from openai import AsyncOpenAI

    logger.info(
        "Initializing OpenAI client"
    )

    return AsyncOpenAI(
        api_key=settings.openai_api_key
    )


# ============================================================
# Vector Store Dependency
# ============================================================


@lru_cache(maxsize=1)
def get_vector_store():
    """
    Returns a singleton vector database client.

    Qdrant connection will be initialized
    during application startup.
    """

    from src.retrieval.vector_store import (
        QdrantVectorStore,
    )

    logger.info(
        "Initializing Qdrant vector store"
    )

    return QdrantVectorStore()


# ============================================================
# Embedding Service Dependency
# ============================================================


@lru_cache(maxsize=1)
def get_embedding_service():
    """
    Returns embedding generation service.

    This will later support:
    - OpenAI embeddings
    - HuggingFace local embeddings
    """

    from src.llm.embeddings import (
        EmbeddingService,
    )

    logger.info(
        "Initializing embedding service"
    )

    return EmbeddingService()


# ============================================================
# Search Provider Dependency
# ============================================================


@lru_cache(maxsize=1)
def get_search_provider():
    """
    Returns configured web search provider.

    Currently:
        Tavily

    Later:
        Brave
        SearXNG
    """

    from src.search.tavily import (
        TavilySearch,
    )

    logger.info(
        "Initializing search provider"
    )

    return TavilySearch()
