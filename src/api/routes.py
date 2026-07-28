from fastapi import APIRouter, HTTPException, status

from src.api.schemas import (
    QueryRequest,
    QueryResponse,
    RetrievalMetadata,
)

from src.config.logging import get_logger


logger = get_logger(__name__)


router = APIRouter(
    prefix="/api/v1",
    tags=["Agentic-RAG"],
)


@router.post(
    "/query",
    response_model=QueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute Agentic RAG query",
)
async def execute_query(
    payload: QueryRequest,
):
    """
    Execute a user query through the Agentic RAG pipeline.

    Flow:

    User Query
        |
        ▼
    Intent Router
        |
        ▼
    Retrieval
        |
        ▼
    Reranking
        |
        ▼
    Generation
        |
        ▼
    Citation Mapping
    """

    logger.info(
        "Received query request"
    )

    try:

        # ------------------------------------------------
        # Temporary response
        #
        # This will be replaced by:
        #
        # agent_service.execute()
        #
        # after LangGraph is implemented.
        # ------------------------------------------------

        answer = (
            "Agentic RAG pipeline is "
            "being initialized."
        )


        return QueryResponse(
            query=payload.query,

            answer=answer,

            metadata=RetrievalMetadata(
                route="local",
                documents_retrieved=0,
                reranked_documents=0,
            ),

            citations=[],

            latency_ms=None,
        )


    except Exception as exc:

        logger.exception(
            "Query execution failed"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Internal Agentic RAG "
                "execution failure"
            ),
        ) from exc
