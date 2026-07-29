"""
Custom exception hierarchy for the Agentic RAG system.

Each module should raise a domain-specific exception
instead of generic Exception whenever possible.
"""


class AgenticRAGError(Exception):
    """
    Base exception for the entire project.
    """

    def __init__(
        self,
        message: str,
    ):
        super().__init__(message)


# ======================================================
# Configuration
# ======================================================

class ConfigurationError(AgenticRAGError):
    """
    Missing or invalid configuration.
    """

    pass


# ======================================================
# LLM
# ======================================================

class LLMError(AgenticRAGError):
    """
    Base exception for LLM-related failures.
    """

    pass


class EmbeddingError(LLMError):
    """
    Failed to generate embeddings.
    """

    pass


class GenerationError(LLMError):
    """
    Failed during answer generation.
    """

    pass


class VerificationError(LLMError):
    """
    Failed during answer verification.
    """

    pass


# ======================================================
# Retrieval
# ======================================================

class RetrievalError(AgenticRAGError):
    """
    Failed during vector retrieval.
    """

    pass


class VectorStoreError(RetrievalError):
    """
    Qdrant operation failed.
    """

    pass


class RerankingError(RetrievalError):
    """
    Cross-encoder reranking failed.
    """

    pass


# ======================================================
# Search
# ======================================================

class SearchError(AgenticRAGError):
    """
    Web search failed.
    """

    pass


class TavilySearchError(SearchError):
    """
    Tavily API failure.
    """

    pass


class BraveSearchError(SearchError):
    """
    Brave Search API failure.
    """

    pass


# ======================================================
# Ingestion
# ======================================================

class IngestionError(AgenticRAGError):
    """
    Base ingestion exception.
    """

    pass


class PDFParsingError(IngestionError):
    """
    PDF parsing failed.
    """

    pass


class ChunkingError(IngestionError):
    """
    Chunk generation failed.
    """

    pass


class IndexingError(IngestionError):
    """
    Vector indexing failed.
    """

    pass


# ======================================================
# API
# ======================================================

class APIError(AgenticRAGError):
    """
    API layer failure.
    """

    pass


class InvalidRequestError(APIError):
    """
    Invalid client request.
    """

    pass


class AuthenticationError(APIError):
    """
    Authentication failure.
    """

    pass
