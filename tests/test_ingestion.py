import pytest

from pathlib import Path


from src.ingestion.chunking import TextChunker
from src.ingestion.metadata import MetadataExtractor



def test_chunk_creation():

    """
    Verify text is split into chunks.
    """


    chunker = TextChunker()



    document = {

        "text":
        (
            "Retrieval augmented generation "
            "combines retrieval systems "
            "with large language models. "
            "This improves factual accuracy."
        )

    }



    chunks = chunker.create_chunks(
        document,
        {}
    )


    assert chunks is not None


    assert len(chunks) > 0



def test_chunk_contains_content():

    chunker = TextChunker()


    document = {

        "text":
        "Transformers use self attention."

    }



    chunks = chunker.create_chunks(

        document,

        {}

    )


    assert (
        "text" in chunks[0]
        or
        "page_content" in chunks[0]
    )



def test_metadata_extraction():

    extractor = MetadataExtractor()



    fake_document = {

        "title":
        "Attention Is All You Need",

        "authors":
        [
            "Ashish Vaswani"
        ]

    }



    fake_path = Path(
        "attention.pdf"
    )



    metadata = extractor.extract(

        fake_document,

        fake_path

    )


    assert metadata is not None


    assert "title" in metadata



def test_pdf_extension_validation():

    file = Path(
        "research_paper.pdf"
    )


    assert file.suffix == ".pdf"
