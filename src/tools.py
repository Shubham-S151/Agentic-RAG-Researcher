import os
from typing import List
from httpx import AsyncClient

async def web_search_tool(query: str, max_results: int = 3) -> List[dict]:
    """Production wrapper for async Tavily Web Search API."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return [{"title": "Error", "url": "", "content": "Tavily API key missing."}]

    async with AsyncClient() as client:
        response = await client.post(
            "https://tavily.com",
            json={"api_key": api_key, "query": query, "max_results": max_results},
            timeout=10.0
        )
        if response.status_code == 200:
            results = response.json().get("results", [])
            return [{"title": r["title"], "url": r["url"], "content": r["content"]} for r in results]
        return []

def cross_encoder_rerank(query: str, documents: List[dict], keep_top_n: int = 3) -> List[dict]:
    """
    Reranks documents using a cross-encoder strategy to drop irrelevant contexts.
    Placeholder demonstrating where to load local HuggingFace cross-encoders or Cohere APIs.
    """
    if not documents:
        return []
    
    # In production, pass text pairs to: AutoModelForSequenceClassification.from_pretrained("BAAI/bge-reranker-large")
    # For structural modularity, sorting by database score dummy calculation here
    sorted_docs = sorted(documents, key=lambda x: x.get("score", 0), reverse=True)
    return sorted_docs[:keep_top_n]
