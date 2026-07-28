from typing import Any, Dict, List, TypedDict


class AgentState(TypedDict):
    """
    Shared state passed between LangGraph nodes.

    Each graph node reads required fields
    and updates specific parts of the state.

    Example:

    Router Node:
        Reads:
            query

        Updates:
            route_decision


    Retrieval Node:
        Reads:
            query

        Updates:
            retrieved_documents
    """

    # ==================================
    # User Request
    # ==================================

    query: str


    # ==================================
    # Routing Decision
    # ==================================

    route_decision: str
    """
    Possible values:

    local
        Answer exists inside research papers

    web
        Requires external information

    hybrid
        Requires both sources
    """


    # ==================================
    # Local Retrieval Results
    # ==================================

    retrieved_documents: List[
        Dict[str, Any]
    ]


    # ==================================
    # Web Search Results
    # ==================================

    web_results: List[
        Dict[str, Any]
    ]


    # ==================================
    # Combined Context
    # ==================================

    compiled_context: str


    # ==================================
    # LLM Output
    # ==================================

    generation: str


    # ==================================
    # Citation Data
    # ==================================

    citation_mappings: List[
        Dict[str, Any]
    ]


    # ==================================
    # Agent Control
    # ==================================

    retry_count: int


    is_hallucination: bool


    # ==================================
    # Observability
    # ==================================

    execution_trace: List[str]
