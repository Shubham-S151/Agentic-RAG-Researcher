import os

from typing import List

from openai import AsyncOpenAI

from src.config.logging import get_logger


logger = get_logger(__name__)


class EmbeddingService:
    """
    Embedding model abstraction.

    Supports:

    - document embeddings
    - query embeddings

    Designed to be replaceable with:

    - HuggingFace models
    - Ollama embeddings
    - vLLM embedding servers
    """



    def __init__(self):

        self.client = AsyncOpenAI(

            api_key=os.getenv(
                "OPENAI_API_KEY"
            )

        )


        self.model = os.getenv(

            "EMBEDDING_MODEL",

            "text-embedding-3-large"

        )



    async def embed_text(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate embedding for one text.
        """


        try:

            response = await self.client.embeddings.create(

                model=self.model,

                input=text,

            )


            vector = (
                response
                .data[0]
                .embedding
            )


            return vector



        except Exception as error:


            logger.error(

                "Embedding generation failed: %s",

                error,

            )


            raise



    async def embed_documents(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        """
        Batch embedding generation.

        Used during indexing.
        """


        if not texts:

            return []



        try:

            response = await self.client.embeddings.create(

                model=self.model,

                input=texts,

            )



            vectors = [

                item.embedding

                for item in response.data

            ]


            logger.info(

                "Generated %s embeddings",

                len(vectors),

            )


            return vectors



        except Exception as error:


            logger.error(

                "Batch embedding failed: %s",

                error,

            )


            raise



    async def embed_query(
        self,
        query: str,
    ) -> List[float]:
        """
        Generate query embedding.

        Separate method because
        production systems often use
        different query/document strategies.
        """


        return await self.embed_text(
            query
        )



# Shared instance

embedding_service = EmbeddingService()
