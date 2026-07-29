import pytest

from httpx import AsyncClient

from src.api.app import app



@pytest.mark.asyncio
async def test_query_endpoint():

    """
    Test successful query execution.
    """

    async with AsyncClient(
        app=app,
        base_url="http://test"
    ) as client:


        response = await client.post(

            "/api/v1/query",

            json={

                "query":
                "Explain retrieval augmented generation."

            }

        )


    assert response.status_code == 200


    data = response.json()


    assert "query" in data


    assert "answer" in data


    assert "route_taken" in data



@pytest.mark.asyncio
async def test_missing_query_field():

    """
    Verify request validation.
    """


    async with AsyncClient(

        app=app,

        base_url="http://test"

    ) as client:


        response = await client.post(

            "/api/v1/query",

            json={}

        )


    assert response.status_code == 422



@pytest.mark.asyncio
async def test_empty_query():

    """
    Ensure API handles empty input.
    """


    async with AsyncClient(

        app=app,

        base_url="http://test"

    ) as client:


        response = await client.post(

            "/api/v1/query",

            json={

                "query": ""

            }

        )


    assert response.status_code in [

        200,

        400

    ]
