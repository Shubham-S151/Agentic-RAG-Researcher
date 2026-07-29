import pytest


from src.retrieval.reranker import (
    rerank_documents
)


from src.retrieval.retriever import (
    Retriever
)



@pytest.fixture
def sample_documents():

    return [

        {
            "text":
            "Transformers use self-attention mechanisms.",

            "metadata":
            {
                "title":
                "Attention Is All You Need",

                "page":
                3
            },

            "score":
            0.85
        },


        {
            "text":
            "Convolutional networks process images.",

            "metadata":
            {
                "title":
                "CNN Survey",

                "page":
                5
            },

            "score":
            0.45
        },


        {
            "text":
            "Retrieval augmented generation combines search and generation.",

            "metadata":
            {
                "title":
                "RAG Survey",

                "page":
                10
            },

            "score":
            0.75
        }

    ]



def test_reranker_returns_top_documents(
    sample_documents
):

    query = (
        "Explain transformer attention"
    )


    results = rerank_documents(

        query,

        sample_documents,

        top_k=2

    )


    assert len(results) == 2


    assert results[0]["score"] >= results[1]["score"]



def test_metadata_preservation(
    sample_documents
):

    query = (
        "Explain transformer architecture"
    )


    results = rerank_documents(

        query,

        sample_documents,

        top_k=1

    )


    document = results[0]


    assert "metadata" in document


    assert "title" in document["metadata"]


    assert "page" in document["metadata"]



@pytest.mark.asyncio
async def test_retriever_initialization():

    retriever = Retriever()


    assert retriever is not None
