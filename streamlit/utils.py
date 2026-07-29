import os

from typing import Dict, Any

import httpx



# -----------------------------------------------------
# Backend Configuration
# -----------------------------------------------------

API_URL = os.getenv(
    "AGENT_API_URL",
    "http://localhost:8000"
)



QUERY_ENDPOINT = (
    f"{API_URL}/api/v1/query"
)



# -----------------------------------------------------
# API Communication
# -----------------------------------------------------

def query_agent(
    query: str,
) -> Dict[str, Any]:
    """
    Sends user query to FastAPI Agentic RAG backend.

    Returns:
        {
            "query": "...",
            "route_taken": "...",
            "answer": "..."
        }
    """


    payload = {

        "query": query

    }


    try:

        response = httpx.post(

            QUERY_ENDPOINT,

            json=payload,

            timeout=120.0

        )


        response.raise_for_status()


        return response.json()



    except httpx.TimeoutException:


        return {

            "answer":
            "The AI engine timed out. Please try again.",

            "route_taken":
            "error",

            "citations":
            []

        }



    except httpx.HTTPStatusError as error:


        return {

            "answer":
            f"Backend error: {error.response.text}",

            "route_taken":
            "error",

            "citations":
            []

        }



    except Exception as error:


        return {

            "answer":
            f"Unexpected error: {str(error)}",

            "route_taken":
            "error",

            "citations":
            []

        }
