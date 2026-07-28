from langgraph.graph import (
    StateGraph,
    START,
    END,
)


from src.graph.state import AgentState


from src.graph.nodes import (
    router_node,
    local_retrieval_node,
    web_search_node,
    context_builder_node,
    generation_node,
    verification_node,
)


from src.graph.edges import (
    router_edge,
    verification_edge,
    retry_counter_edge,
)



# =====================================
# Create Graph
# =====================================

workflow = StateGraph(
    AgentState
)



# =====================================
# Register Nodes
# =====================================

workflow.add_node(
    "router",
    router_node,
)


workflow.add_node(
    "local_retrieval",
    local_retrieval_node,
)


workflow.add_node(
    "web_search",
    web_search_node,
)


workflow.add_node(
    "context_builder",
    context_builder_node,
)


workflow.add_node(
    "generation",
    generation_node,
)


workflow.add_node(
    "verification",
    verification_node,
)



# =====================================
# Entry Point
# =====================================

workflow.add_edge(
    START,
    "router",
)



# =====================================
# Router Branching
# =====================================

workflow.add_conditional_edges(

    "router",

    router_edge,

    {

        "local_retrieval":
            "local_retrieval",


        "web_search":
            "web_search",


        "hybrid":
            "local_retrieval",
    },
)



# =====================================
# Local Retrieval Flow
# =====================================

workflow.add_edge(

    "local_retrieval",

    "context_builder",

)



# =====================================
# Web Retrieval Flow
# =====================================

workflow.add_edge(

    "web_search",

    "context_builder",

)



# =====================================
# Hybrid Connection
# =====================================

"""
Hybrid execution requires:

Local retrieval
        |
        ▼
Web search
        |
        ▼
Context builder


This simple version starts with
local retrieval and then expands
through the next graph revision.
"""


workflow.add_edge(

    "context_builder",

    "generation",

)



# =====================================
# Generation Verification
# =====================================

workflow.add_edge(

    "generation",

    "verification",

)



# =====================================
# Verification Routing
# =====================================

workflow.add_conditional_edges(

    "verification",

    verification_edge,

    {

        "complete":
            END,


        "retry_generation":
            "generation",
    },
)



# =====================================
# Compile Runtime Agent
# =====================================

runtime_agent = workflow.compile()
