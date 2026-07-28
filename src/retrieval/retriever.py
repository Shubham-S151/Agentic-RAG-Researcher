from typing import Any, Dict, List, Optional

from src.config.logging import get_logger
from src.config.settings import settings
from src.llm.embeddings import EmbeddingService
from src.retrieval.vector_store import QdrantVectorStore


logger = get_logger(__name__)


class Retriever:
    """
    High-level retrieval pipeline.

    Responsibilities:

    1. Convert query into embedding
    2. Search vector database
    3. Return relevant documents

    Does not:
    - rerank
    - generate answers
    - call external search
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: QdrantVectorStore,
    ):
        self.embedding_service = (
            embedding_service
        )

        self.vector_store = (
            vector_store
        )

        self.top_k = (
            settings.top_k_retrieval
        )


    async def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant document chunks.

        Args:

            query:
                User question.

            top_k:
                Number of documents returned.

            filters:
                Optional metadata filters.

        Returns:

            List of retrieved chunks.
        """

        if not query.strip():
            raise ValueError(
                "Query cannot be empty"
            )


        logger.info(
            "Starting retrieval for query"
        )


        # -----------------------------------------
        # Step 1:
        # Convert query into vector
        # -----------------------------------------

        query_vector = (
            await self.embedding_service.embed_text(
                query
            )
        )


        # -----------------------------------------
        # Step 2:
        # Semantic search
        # -----------------------------------------

        documents = (
            await self.vector_store.similarity_search(
                query_vector=query_vector,
                top_k=(
                    top_k
                    or self.top_k
                ),
                filters=filters,
            )
        )


        logger.info(
            "Retrieved %s documents",
            len(documents),
        )


        return documents
