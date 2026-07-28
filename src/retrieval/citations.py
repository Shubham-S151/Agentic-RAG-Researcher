from typing import Any, Dict, List

from src.config.logging import get_logger


logger = get_logger(__name__)


class CitationBuilder:
    """
    Converts retrieved document metadata
    into structured citation objects.

    Responsible for:
    - metadata extraction
    - citation numbering
    - source formatting
    """


    def build(
        self,
        documents: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Create citation mappings.

        Input example:

        {
            "text": "...",
            "metadata": {
                "title": "...",
                "page_number": 3,
                "doi": "..."
            }
        }


        Output:

        [
          {
            "citation_id":1,
            "title":"...",
            "page":3
          }
        ]

        """


        citations = []


        for index, document in enumerate(
            documents,
            start=1,
        ):

            metadata = (
                document.get(
                    "metadata",
                    {}
                )
            )


            citation = {

                "citation_id": index,


                "title": (
                    metadata.get(
                        "title",
                        "Unknown"
                    )
                ),


                "authors": (
                    metadata.get(
                        "authors",
                        []
                    )
                ),


                "page_number": (
                    metadata.get(
                        "page_number"
                    )
                ),


                "doi": (
                    metadata.get(
                        "doi"
                    )
                ),


                "source_type": "paper",
            }


            citations.append(
                citation
            )


        logger.info(
            "Generated %s citations",
            len(citations),
        )


        return citations



    def format_prompt_sources(
        self,
        citations: List[Dict[str, Any]],
    ) -> str:
        """
        Converts citations into LLM context.

        The model receives verified
        sources instead of creating them.
        """


        source_text = ""


        for citation in citations:

            source_text += (
                f"[{citation['citation_id']}] "
                f"{citation['title']}"
            )


            if citation.get(
                "page_number"
            ):

                source_text += (
                    f", Page "
                    f"{citation['page_number']}"
                )


            if citation.get(
                "doi"
            ):

                source_text += (
                    f", DOI: "
                    f"{citation['doi']}"
                )


            source_text += "\n"


        return source_text



    def attach_citations(
        self,
        answer: str,
        citations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Final API response formatter.
        """


        return {

            "answer": answer,

            "citations": citations,

        }
