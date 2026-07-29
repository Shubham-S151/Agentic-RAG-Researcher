import pytest


from src.graph.nodes import (
    synthesis_generation_node
)



@pytest.mark.asyncio
async def test_generation_with_context():

    """
    Test answer generation when retrieved
    documents are available.
    """


    state = {


        "query":
        "Explain transformer architecture.",



        "retrieved_documents":

        [

            {

                "text":
                (
                    "Transformers use "
                    "self-attention mechanisms "
                    "to process sequences."
                ),


                "metadata":
                {

                    "title":
                    "Attention Is All You Need",


                    "page":
                    3

                }

            }

        ],



        "web_results": []

    }



    result = await synthesis_generation_node(
        state
    )


    assert result is not None


    assert "generation" in result


    assert len(
        result["generation"]
    ) > 0



@pytest.mark.asyncio
async def test_generation_with_web_context():

    """
    Test generation using web search results.
    """


    state = {


        "query":
        "Latest developments in RAG.",



        "retrieved_documents":
        [],



        "web_results":

        [

            {

                "title":
                "Recent RAG Research",


                "url":
                "https://example.com",


                "content":
                "New retrieval techniques improve accuracy."

            }

        ]

    }



    result = await synthesis_generation_node(
        state
    )


    assert "generation" in result



@pytest.mark.asyncio
async def test_generation_empty_context():

    """
    Verify graceful handling when no context exists.
    """


    state = {


        "query":
        "Unknown question",


        "retrieved_documents":
        [],


        "web_results": []

    }



    result = await synthesis_generation_node(
        state
    )


    assert "generation" in result


    assert isinstance(
        result["generation"],
        str
    )
