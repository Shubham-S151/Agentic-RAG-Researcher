import json
from typing import Dict, Any

from src.graph.state import AgentState

from src.llm.openai_client import llm_client

from src.retrieval.retriever import Retriever
from src.retrieval.citations import CitationBuilder

from src.search.tavily import TavilySearch

from src.config.logging import get_logger


logger = get_logger(__name__)


# =====================================
# Shared Services
# =====================================

retriever = Retriever()

citation_builder = CitationBuilder()

web_search = TavilySearch()



# =====================================
# 1. Intent Router Node
# =====================================

async def router_node(
    state: AgentState,
) -> Dict[str, Any]:
    """
    Decide whether query needs:

    - local documents
    - web search
    - both
    """


    prompt = f"""
You are an intelligent routing system.

Analyze this user query:

{state["query"]}


Choose exactly one:

local:
Question can be answered using research papers.

web:
Question requires current external information.

hybrid:
Question requires both.


Return JSON only:

{{
 "route": "local | web | hybrid"
}}
"""


    response = await llm_client.chat(
        prompt
    )


    result = json.loads(
        response
    )


    route = result.get(
        "route",
        "hybrid"
    )


    logger.info(
        "Query routed to %s",
        route,
    )


    return {

        "route_decision":
            route,

        "execution_trace":
            state.get(
                "execution_trace",
                []
            )
            +
            [
                f"router:{route}"
            ]
    }



# =====================================
# 2. Local Retrieval Node
# =====================================

async def local_retrieval_node(
    state: AgentState,
) -> Dict[str, Any]:
    """
    Retrieve relevant research papers
    from vector database.
    """


    documents = await retriever.retrieve(
        query=state["query"]
    )


    return {

        "retrieved_documents":
            documents,


        "execution_trace":
            state.get(
                "execution_trace",
                []
            )
            +
            [
                "local_retrieval:complete"
            ]
    }



# =====================================
# 3. Web Search Node
# =====================================

async def web_search_node(
    state: AgentState,
) -> Dict[str, Any]:
    """
    Retrieve live internet context.
    """


    results = await web_search.search(
        query=state["query"]
    )


    return {

        "web_results":
            results,


        "execution_trace":
            state.get(
                "execution_trace",
                []
            )
            +
            [
                "web_search:complete"
            ]
    }



# =====================================
# 4. Context Builder Node
# =====================================

async def context_builder_node(
    state: AgentState,
) -> Dict[str, Any]:
    """
    Merge retrieved information into
    a clean LLM context window.
    """


    context = ""


    documents = state.get(
        "retrieved_documents",
        []
    )


    if documents:

        context += (
            "\n\n"
            "=== Research Papers ===\n"
        )


        for index, doc in enumerate(
            documents,
            start=1,
        ):

            context += (
                f"\n[{index}] "
                f"{doc['text']}"
            )



    web_results = state.get(
        "web_results",
        []
    )


    if web_results:

        context += (
            "\n\n"
            "=== Web Sources ===\n"
        )


        for result in web_results:

            context += (
                f"\n"
                f"{result['title']}"
                "\n"
                f"{result['content']}"
            )



    return {

        "compiled_context":
            context,


        "execution_trace":
            state.get(
                "execution_trace",
                []
            )
            +
            [
                "context_builder:complete"
            ]
    }



# =====================================
# 5. Generation Node
# =====================================

async def generation_node(
    state: AgentState,
) -> Dict[str, Any]:
    """
    Generate final grounded answer.
    """


    prompt = f"""

Answer the user query using ONLY
the provided context.


Context:

{state["compiled_context"]}


Question:

{state["query"]}


Rules:

- Do not invent facts.
- Cite sources.
- If context is insufficient,
say so.
"""


    answer = await llm_client.chat(
        prompt
    )


    citations = (
        citation_builder.build(
            state.get(
                "retrieved_documents",
                []
            )
        )
    )


    return {

        "generation":
            answer,


        "citation_mappings":
            citations,


        "execution_trace":
            state.get(
                "execution_trace",
                []
            )
            +
            [
                "generation:complete"
            ]
    }



# =====================================
# 6. Verification Node
# =====================================

async def verification_node(
    state: AgentState,
) -> Dict[str, Any]:
    """
    Basic hallucination checker.

    Production upgrade:

    - Ragas
    - NLI models
    - LLM judge
    """


    answer = state.get(
        "generation",
        ""
    )


    context = state.get(
        "compiled_context",
        ""
    )


    hallucination = False


    if (
        len(answer) > 0
        and len(context) == 0
    ):

        hallucination = True



    return {

        "is_hallucination":
            hallucination,


        "execution_trace":
            state.get(
                "execution_trace",
                []
            )
            +
            [
                "verification:complete"
            ]
    }
