import os
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams

class QdrantVectorStore:
    def __init__(self):
        self.client = AsyncQdrantClient(
            url=os.getenv("QDRANT_URL", "http://localhost:6333"),
            api_key=os.getenv("QDRANT_API_KEY", None),
            timeout=30.0
        )
        self.collection_name = "research_papers"

    async def initialize_collection(self, vector_size: int = 1024):
        """Creates collection if it doesn't exist (e.g., for BGE-large vectors)."""
        exists = await self.client.collection_exists(self.collection_name)
        if not exists:
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

    async def semantic_search(self, query_vector: List[float], top_k: int = 5) -> List[dict]:
        """Performs fast semantic lookup with structured metadata extraction."""
        search_results = await self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True
        )
        return [
            {
                "text": hit.payload.get("page_content", ""),
                "metadata": {
                    "title": hit.payload.get("title", "Unknown"),
                    "doi": hit.payload.get("doi", "N/A"),
                    "page": hit.payload.get("page_number", 0)
                },
                "score": hit.score
            }
            for hit in search_results
        ]
