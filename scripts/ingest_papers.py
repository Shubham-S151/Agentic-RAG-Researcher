"""
Paper ingestion pipeline runner.

Usage:

python scripts/ingest_papers.py

Pipeline:

PDF
 |
Parser
 |
Chunker
 |
Metadata
 |
Indexer
 |
Qdrant
"""


import asyncio

from pathlib import Path

from src.ingestion.parser import PDFParser
from src.ingestion.chunking import TextChunker
from src.ingestion.metadata import MetadataExtractor
from src.ingestion.indexer import PaperIndexer

from src.config.logging import get_logger



logger = get_logger(__name__)



PAPER_DIRECTORY = Path(
    "data/papers"
)



async def ingest_single_paper(
    pdf_path: Path,
    parser: PDFParser,
    chunker: TextChunker,
    metadata_extractor: MetadataExtractor,
    indexer: PaperIndexer,
):
    """
    Process one research paper.
    """


    logger.info(
        "Processing paper: %s",
        pdf_path.name
    )


    # ----------------------------------
    # Extract PDF content
    # ----------------------------------

    document = await parser.parse(
        pdf_path
    )


    # ----------------------------------
    # Extract metadata
    # ----------------------------------

    metadata = metadata_extractor.extract(
        document,
        pdf_path
    )


    # ----------------------------------
    # Create hierarchical chunks
    # ----------------------------------

    chunks = chunker.create_chunks(
        document,
        metadata
    )


    # ----------------------------------
    # Store embeddings + metadata
    # ----------------------------------

    await indexer.index_documents(
        chunks
    )


    logger.info(
        "Completed: %s",
        pdf_path.name
    )



async def main():

    if not PAPER_DIRECTORY.exists():

        raise FileNotFoundError(
            f"{PAPER_DIRECTORY} does not exist"
        )


    parser = PDFParser()


    chunker = TextChunker()


    metadata_extractor = MetadataExtractor()


    indexer = PaperIndexer()



    papers = list(
        PAPER_DIRECTORY.glob(
            "*.pdf"
        )
    )


    if not papers:

        logger.warning(
            "No PDF files found."
        )

        return



    logger.info(
        "Found %s papers",
        len(papers)
    )



    for paper in papers:

        await ingest_single_paper(

            paper,

            parser,

            chunker,

            metadata_extractor,

            indexer,

        )



    logger.info(
        "All papers indexed successfully."
    )



if __name__ == "__main__":

    asyncio.run(
        main()
    )
