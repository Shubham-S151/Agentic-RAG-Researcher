from typing import List, TypedDict, Optional

class AgentState(TypedDict):
    """Tracks the state across the agentic execution loop."""
    query: str
    route_decision: str  # "local", "web", or "hybrid"
    retrieved_documents: List[dict]
    web_results: List[dict]
    compiled_context: str
    generation: str
    citation_mappings: List[dict]
    retry_count: int
    is_hallucination: bool
