from typing import Any, Dict, List
from uuid import uuid4

from src.config.logging import get_logger


logger = get_logger(__name__)


class HierarchicalChunker:
    """
    Parent-child document chunking strategy.

    Parent chunks:
        Preserve full section context.

    Child chunks:
        Optimized for vector retrieval.
    """


    def __init__(
        self,
        child_chunk_size: int = 500,
        child_overlap: int = 100,
    ):

        self.child_chunk_size = (
            child_chunk_size
        )

        self.child_overlap = (
            child_overlap
        )


    def create_chunks(
        self,
        pages: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Convert parsed pages into
        hierarchical chunks.

        Input:

        [
          {
            "page_number":1,
            "text":"..."
          }
        ]

        Output:

        [
          {
            "id":"...",
            "parent_id":"...",
            "text":"...",
            "metadata":{}
          }
        ]
        """


        chunks = []


        for page in pages:

            parent_id = str(
                uuid4()
            )


            parent_text = (
                page["text"]
            )


            parent_chunk = {

                "id": parent_id,

                "type": "parent",

                "text": parent_text,

                "metadata": {

                    "page_number":
                        page["page_number"],

                },
            }


            children = (
                self._split_text(
                    parent_text
                )
            )


            for child_text in children:

                child_chunk = {

                    "id": str(
                        uuid4()
                    ),

                    "parent_id":
                        parent_id,

                    "type":
                        "child",

                    "text":
                        child_text,

                    "metadata": {

                        "page_number":
                            page[
                                "page_number"
                            ],

                        "parent_id":
                            parent_id,
                    },
                }


                chunks.append(
                    child_chunk
                )


        logger.info(
            "Created %s child chunks",
            len(chunks),
        )


        return chunks



    def _split_text(
        self,
        text: str,
    ) -> List[str]:
        """
        Sliding-window text splitter.

        Keeps overlap between chunks.
        """


        words = (
            text.split()
        )


        chunks = []


        start = 0


        while start < len(words):

            end = (
                start
                +
                self.child_chunk_size
            )


            chunk_words = (
                words[start:end]
            )


            chunks.append(
                " ".join(
                    chunk_words
                )
            )


            start = (
                end
                -
                self.child_overlap
            )


        return chunks
