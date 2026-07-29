import uuid

from typing import List, Dict, Any

from src.llm.embeddings import embedding_service
from src.retrieval.vector_store import vector_store
from src.config.logging import get_logger

logger = get_logger(__name__)


class DocumentIndexer:
    """
    Index processed document chunks into Qdrant.

    Responsibilities:
        - Generate embeddings
        - Prepare payloads
        - Upload vectors
    """

    async def index_documents(
        self,
        chunks: List[Dict[str, Any]],
    ) -> None:
        """
        Index processed document chunks.

        Expected chunk format:

        {
            "text": "...",
            "metadata": {
                ...
            }
        }
        """

        if not chunks:
            logger.warning("No chunks received for indexing.")
            return

        logger.info(
            "Generating embeddings for %d chunks.",
            len(chunks),
        )

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        vectors = await embedding_service.embed_documents(
            texts
        )

        documents = []

        for chunk, vector in zip(chunks, vectors):

            metadata = chunk.get(
                "metadata",
                {},
            )

            payload = {
                "text": chunk["text"],
                "title": metadata.get("title"),
                "authors": metadata.get("authors"),
                "page": metadata.get("page"),
                "doi": metadata.get("doi"),
                "section": metadata.get("section"),
                "chunk_id": metadata.get("chunk_id"),
            }

            documents.append(
                {
                    "id": str(uuid.uuid4()),
                    "vector": vector,
                    "payload": payload,
                }
            )

        logger.info(
            "Uploading %d vectors to Qdrant.",
            len(documents),
        )

        await vector_store.insert_documents(
            documents
        )

        logger.info(
            "Indexing completed successfully."
        )


document_indexer = DocumentIndexer()
