from typing import Any, Dict, List, Optional

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from src.config.logging import get_logger
from src.config.settings import settings


logger = get_logger(__name__)


class QdrantVectorStore:
    """
    Production wrapper around Qdrant.

    Responsibilities:

    - Initialize collections
    - Insert vectors
    - Search vectors
    - Handle metadata payloads

    The rest of the application never
    interacts directly with Qdrant.
    """


    def __init__(
        self,
        client: Optional[AsyncQdrantClient] = None,
    ):

        self.client = (
            client
            if client
            else AsyncQdrantClient(
                url=settings.qdrant_url,
                api_key=(
                    settings.qdrant_api_key
                    or None
                ),
                timeout=30,
            )
        )


        self.collection_name = (
            settings.qdrant_collection
        )

        self.vector_dimension = (
            settings.embedding_dimension
        )


    async def initialize_collection(
        self,
    ) -> None:
        """
        Create Qdrant collection if missing.

        Called during application startup.
        """

        exists = await (
            self.client
            .collection_exists(
                self.collection_name
            )
        )


        if exists:
            logger.info(
                "Qdrant collection already exists"
            )
            return


        logger.info(
            "Creating Qdrant collection: %s",
            self.collection_name,
        )


        await self.client.create_collection(

            collection_name=(
                self.collection_name
            ),

            vectors_config=VectorParams(

                size=self.vector_dimension,

                distance=Distance.COSINE,
            ),
        )


    async def insert_documents(
        self,
        documents: List[Dict[str, Any]],
    ) -> None:
        """
        Insert embedded documents.

        Expected format:

        {
            "id": "...",
            "vector": [...],
            "payload": {
                "text": "...",
                "title": "...",
                "page": 3
            }
        }
        """


        points = []


        for document in documents:

            points.append(

                PointStruct(

                    id=document["id"],

                    vector=document["vector"],

                    payload=document["payload"],
                )
            )


        await self.client.upsert(

            collection_name=(
                self.collection_name
            ),

            points=points,
        )


        logger.info(
            "Inserted %s documents into Qdrant",
            len(points),
        )


    async def similarity_search(
        self,
        query_vector: List[float],
        top_k: int = 20,
        filters: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic similarity search.
        """


        results = await self.client.search(

            collection_name=(
                self.collection_name
            ),

            query_vector=query_vector,

            limit=top_k,

            query_filter=filters,

            with_payload=True,
        )


        documents = []


        for result in results:

            payload = (
                result.payload
                or {}
            )


            documents.append(
                {
                    "id": result.id,

                    "score": result.score,

                    "text": (
                        payload.get(
                            "text",
                            ""
                        )
                    ),

                    "metadata": {
                        "title": payload.get(
                            "title",
                            "Unknown"
                        ),

                        "authors": payload.get(
                            "authors",
                            []
                        ),

                        "page_number": payload.get(
                            "page_number"
                        ),

                        "doi": payload.get(
                            "doi"
                        ),
                    },
                }
            )


        return documents


    async def health_check(self) -> bool:
        """
        Check Qdrant availability.
        """

        try:

            await self.client.get_collections()

            return True


        except Exception:

            logger.exception(
                "Qdrant health check failed"
            )

            return False
