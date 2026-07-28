from src.graph.state import AgentState


def router_edge(
    state: AgentState,
) -> str:
    """
    Determines next execution path
    after router node.

    Returns:

        local_retrieval
        web_search
        hybrid
    """


    decision = (
        state.get(
            "route_decision",
            "hybrid",
        )
    )


    if decision == "local":

        return "local_retrieval"



    if decision == "web":

        return "web_search"



    return "hybrid"



def hybrid_edge(
    state: AgentState,
) -> str:
    """
    Controls hybrid execution.

    Hybrid means:

    1. Retrieve internal papers
    2. Retrieve external sources

    """

    return "local_retrieval"



def verification_edge(
    state: AgentState,
) -> str:
    """
    Decide whether answer is accepted
    or requires regeneration.
    """


    hallucination = (
        state.get(
            "is_hallucination",
            False,
        )
    )


    retries = (
        state.get(
            "retry_count",
            0,
        )
    )


    max_retries = 2



    if hallucination and retries < max_retries:

        return "retry_generation"



    return "complete"



def retry_counter_edge(
    state: AgentState,
) -> dict:
    """
    Increment retry counter
    before regeneration.
    """


    return {

        "retry_count":
            state.get(
                "retry_count",
                0,
            )
            + 1
    }
