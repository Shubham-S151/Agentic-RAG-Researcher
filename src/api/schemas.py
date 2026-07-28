from typing import List, Literal, Optional

from pydantic import BaseModel, Field


# ============================================================
# Query Request
# ============================================================


class QueryRequest(BaseModel):
    """
    Incoming user query request.
    """

    query: str = Field(
        ...,
        min_length=3,
        max_length=5000,
        description="User question for the RAG agent",
    )


    conversation_id: Optional[str] = Field(
        default=None,
        description=(
            "Optional identifier for maintaining "
            "conversation context"
        ),
    )


# ============================================================
# Citation Models
# ============================================================


class Citation(BaseModel):
    """
    Represents a source citation.

    Can represent:
    - Research paper chunks
    - Web sources
    """

    title: str = Field(
        description="Source title"
    )

    source_type: Literal[
        "paper",
        "web",
    ]

    page_number: Optional[int] = Field(
        default=None,
        description="PDF page number if available",
    )

    url: Optional[str] = Field(
        default=None,
        description="Web URL if source is external",
    )

    doi: Optional[str] = Field(
        default=None,
        description="Research paper DOI",
    )


# ============================================================
# Retrieval Metadata
# ============================================================


class RetrievalMetadata(BaseModel):
    """
    Information about retrieval execution.
    """

    route: Literal[
        "local",
        "web",
        "hybrid",
    ]

    documents_retrieved: int = 0

    reranked_documents: int = 0


# ============================================================
# Agent Response
# ============================================================


class QueryResponse(BaseModel):
    """
    Final API response returned to clients.
    """

    query: str

    answer: str

    metadata: RetrievalMetadata

    citations: List[Citation] = Field(
        default_factory=list
    )

    latency_ms: Optional[float] = None


# ============================================================
# Streaming Response Event
# ============================================================


class StreamEvent(BaseModel):
    """
    Server-Sent Event payload.

    Used for token streaming.
    """

    event: Literal[
        "token",
        "citation",
        "metadata",
        "complete",
        "error",
    ]

    data: str


# ============================================================
# Health Check Schemas
# ============================================================


class HealthResponse(BaseModel):
    """
    Service health response.
    """

    status: Literal[
        "healthy",
        "unhealthy",
    ]

    service: str

    version: str
