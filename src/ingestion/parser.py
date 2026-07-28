from pathlib import Path
from typing import Any, Dict, List

from src.config.logging import get_logger


logger = get_logger(__name__)


class PDFParser:
    """
    Research paper PDF parser.

    Current implementation:
        Local PDF extraction wrapper.

    Can later support:
        - Marker
        - LlamaParse
        - Unstructured.io
    """


    def __init__(
        self,
        parser_type: str = "marker",
    ):

        self.parser_type = parser_type


    async def parse(
        self,
        file_path: str,
    ) -> Dict[str, Any]:
        """
        Parse PDF into structured representation.


        Returns:

        {
            "pages": [
                {
                    "page_number":1,
                    "text":"..."
                }
            ],

            "metadata":{
                "filename":"..."
            }
        }

        """


        path = Path(file_path)


        if not path.exists():

            raise FileNotFoundError(
                f"PDF not found: {file_path}"
            )


        logger.info(
            "Parsing PDF: %s",
            file_path,
        )


        if self.parser_type == "marker":

            pages = await self._marker_parse(
                path
            )

        else:

            pages = await self._basic_parse(
                path
            )


        return {

            "pages": pages,

            "metadata": {
                "filename": path.name,
                "parser": self.parser_type,
            },
        }



    async def _marker_parse(
        self,
        path: Path,
    ) -> List[Dict[str, Any]]:
        """
        Marker parser integration point.

        Marker preserves:
        - tables
        - equations
        - headings
        - layout
        """

        # Placeholder until dependency
        # is installed.

        return await self._basic_parse(
            path
        )



    async def _basic_parse(
        self,
        path: Path,
    ) -> List[Dict[str, Any]]:
        """
        Fallback PDF extraction.

        Used only for development.

        Production should use:
        Marker/LlamaParse.
        """


        try:

            import pypdf


            reader = (
                pypdf.PdfReader(
                    str(path)
                )
            )


            pages = []


            for index, page in enumerate(
                reader.pages,
                start=1,
            ):

                text = (
                    page.extract_text()
                    or ""
                )


                pages.append(
                    {
                        "page_number": index,

                        "text": text,
                    }
                )


            return pages


        except Exception:

            logger.exception(
                "PDF parsing failed"
            )

            raise
