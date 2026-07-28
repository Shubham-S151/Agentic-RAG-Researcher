import re
from typing import Any, Dict, Optional

from src.config.logging import get_logger


logger = get_logger(__name__)


class MetadataExtractor:
    """
    Extracts and normalizes research paper metadata.

    Handles:

    - title
    - authors
    - DOI
    - publication year
    - source information
    """


    DOI_PATTERN = (
        r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+"
    )


    YEAR_PATTERN = (
        r"\b(19|20)\d{2}\b"
    )


    def extract(
        self,
        document_text: str,
        existing_metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Dict[str, Any]:
        """
        Extract metadata from document.

        Existing metadata from PDF parser
        is preserved.
        """


        metadata = (
            existing_metadata.copy()
            if existing_metadata
            else {}
        )


        metadata.update(

            {

                "title":
                    self.extract_title(
                        document_text
                    ),


                "doi":
                    self.extract_doi(
                        document_text
                    ),


                "publication_year":
                    self.extract_year(
                        document_text
                    ),


                "authors":
                    self.extract_authors(
                        document_text
                    ),

            }
        )


        return metadata



    def extract_title(
        self,
        text: str,
    ) -> str:
        """
        Basic title extraction.

        Production upgrade:
        use GROBID or LLM extraction.
        """


        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]


        if lines:

            return lines[0][:300]


        return "Unknown Title"



    def extract_doi(
        self,
        text: str,
    ) -> Optional[str]:
        """
        Extract DOI identifier.
        """


        match = re.search(
            self.DOI_PATTERN,
            text,
        )


        if match:

            return match.group(0)


        return None



    def extract_year(
        self,
        text: str,
    ) -> Optional[int]:
        """
        Extract publication year.
        """


        match = re.search(
            self.YEAR_PATTERN,
            text,
        )


        if match:

            return int(
                match.group(0)
            )


        return None



    def extract_authors(
        self,
        text: str,
    ) -> list[str]:
        """
        Placeholder author extraction.

        Production options:

        - GROBID
        - Semantic Scholar API
        - Crossref API
        """


        return []
