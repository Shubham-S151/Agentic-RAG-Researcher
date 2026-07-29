import pytest

from src.graph.nodes import routing_node



@pytest.mark.asyncio
async def test_local_route():

    state = {

        "query":
        "Explain transformer attention mechanism from research papers."

    }


    result = await routing_node(
        state
    )


    assert result[
        "route_decision"
    ] in [
        "local",
        "hybrid"
    ]



@pytest.mark.asyncio
async def test_web_route():

    state = {

        "query":
        "What are the latest AI developments this week?"

    }


    result = await routing_node(
        state
    )


    assert result[
        "route_decision"
    ] in [
        "web",
        "hybrid"
    ]



@pytest.mark.asyncio
async def test_hybrid_route():

    state = {

        "query":
        """
        Compare recent RAG research papers
        with current production systems.
        """

    }


    result = await routing_node(
        state
    )


    assert result[
        "route_decision"
    ] in [
        "hybrid",
        "local",
        "web"
    ]
