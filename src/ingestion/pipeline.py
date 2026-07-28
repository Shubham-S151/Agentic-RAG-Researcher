from typing import Any, Dict, List
from uuid import uuid4

from src.config.logging import get_logger

from src.ingestion.parser import PDFParser
from src.ingestion.metadata import MetadataExtractor
from src.ingestion.chunker import HierarchicalChunker

from src.llm.embeddings import EmbeddingService

from src.retrieval.vector_store import (
    QdrantVectorStore,
)


logger = get_logger(__name__)


class IngestionPipeline:
    """
    Complete document ingestion workflow.

    Flow:

    PDF
     |
     ▼
    Parser
     |
     ▼
    Metadata
     |
     ▼
    Chunking
     |
     ▼
    Embeddings
     |
     ▼
    Vector Database
    """


    def __init__(
        self,
        parser: PDFParser,
        metadata_extractor: MetadataExtractor,
        chunker: HierarchicalChunker,
        embedding_service: EmbeddingService,
        vector_store: QdrantVectorStore,
    ):

        self.parser = parser

        self.metadata_extractor = (
            metadata_extractor
        )

        self.chunker = chunker

        self.embedding_service = (
            embedding_service
        )

        self.vector_store = (
            vector_store
        )


    async def ingest(
        self,
        file_path: str,
    ) -> Dict[str, Any]:
        """
        Execute complete ingestion pipeline.

        Returns ingestion statistics.
        """


        logger.info(
            "Starting ingestion: %s",
            file_path,
        )


        # -------------------------------------
        # Step 1:
        # Parse PDF
        # -------------------------------------

        parsed_document = (
            await self.parser.parse(
                file_path
            )
        )


        pages = (
            parsed_document["pages"]
        )


        # -------------------------------------
        # Step 2:
        # Extract metadata
        # -------------------------------------

        full_text = "\n".join(
            [
                page["text"]
                for page in pages
            ]
        )


        metadata = (
            self.metadata_extractor.extract(
                document_text=full_text,
                existing_metadata=(
                    parsed_document[
                        "metadata"
                    ]
                ),
            )
        )


        # -------------------------------------
        # Step 3:
        # Create chunks
        # -------------------------------------

        chunks = (
            self.chunker.create_chunks(
                pages
            )
        )


        # Attach document metadata
        for chunk in chunks:

            chunk["metadata"].update(
                metadata
            )


        # -------------------------------------
        # Step 4:
        # Generate embeddings
        # -------------------------------------

        texts = [
            chunk["text"]
            for chunk in chunks
        ]


        vectors = (
            await self.embedding_service
            .embed_documents(
                texts
            )
        )


        # -------------------------------------
        # Step 5:
        # Prepare Qdrant points
        # -------------------------------------

        documents = []


        for chunk, vector in zip(
            chunks,
            vectors,
        ):

            documents.append(

                {

                    "id": str(
                        uuid4()
                    ),

                    "vector": vector,


                    "payload": {

                        "text":
                            chunk["text"],


                        "parent_id":
                            chunk.get(
                                "parent_id"
                            ),


                        **chunk[
                            "metadata"
                        ],
                    },
                }
            )


        # -------------------------------------
        # Step 6:
        # Store vectors
        # -------------------------------------

        await (
            self.vector_store
            .insert_documents(
                documents
            )
        )


        result = {

            "file":
                file_path,


            "pages_processed":
                len(pages),


            "chunks_created":
                len(chunks),


            "vectors_inserted":
                len(documents),


            "metadata":
                metadata,
        }


        logger.info(
            "Ingestion complete: %s",
            result,
        )


        return result
