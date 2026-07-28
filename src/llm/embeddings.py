from typing import List

from openai import AsyncOpenAI

from src.config.logging import get_logger
from src.config.settings import settings


logger = get_logger(__name__)


class EmbeddingService:
    """
    Service responsible for generating vector embeddings.

    Supports:
    - Single text embedding
    - Batch embedding

    Current provider:
        OpenAI text-embedding-3-large
    """


    def __init__(
        self,
        client: AsyncOpenAI | None = None,
    ):

        self.client = client or AsyncOpenAI(
            api_key=settings.openai_api_key
        )

        self.model = (
            settings.embedding_model
        )

        self.dimension = (
            settings.embedding_dimension
        )


    async def embed_text(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate embedding for a single text.

        Used for:
        - User queries
        - Small document chunks
        """

        if not text.strip():
            raise ValueError(
                "Cannot embed empty text"
            )


        response = await self.client.embeddings.create(

            model=self.model,

            input=text,
        )


        vector = (
            response
            .data[0]
            .embedding
        )


        self._validate_dimension(
            vector
        )


        return vector


    async def embed_documents(
        self,
        documents: List[str],
        batch_size: int = 100,
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.

        Batch processing is important during
        PDF ingestion because research papers
        may contain thousands of chunks.
        """


        if not documents:
            return []


        embeddings = []


        for start in range(
            0,
            len(documents),
            batch_size,
        ):

            batch = documents[
                start:start + batch_size
            ]


            logger.info(
                "Embedding batch %s-%s",
                start,
                start + len(batch),
            )


            response = (
                await self.client.embeddings.create(
                    model=self.model,
                    input=batch,
                )
            )


            batch_vectors = [
                item.embedding
                for item in response.data
            ]


            embeddings.extend(
                batch_vectors
            )


        for vector in embeddings:
            self._validate_dimension(
                vector
            )


        return embeddings


    def _validate_dimension(
        self,
        vector: List[float],
    ) -> None:
        """
        Ensures embedding size matches
        Qdrant collection configuration.
        """

        if len(vector) != self.dimension:

            raise ValueError(
                (
                    "Embedding dimension mismatch. "
                    f"Expected {self.dimension}, "
                    f"received {len(vector)}"
                )
            )
