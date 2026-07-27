import json
from openai import AsyncOpenAI
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.database import QdrantVectorStore
from src.tools import web_search_tool, cross_encoder_rerank

llm_client = AsyncOpenAI() # Automatically looks for OPENAI_API_KEY
db = QdrantVectorStore()

async def routing_node(state: AgentState) -> dict:
    '''Classifies user intent to choose structural execution branch.'''
    prompt = f'''Analyze the query: "{state['query']}". 
    Determine if it requires:
    1. 'local' (Specific structural engineering/academic facts likely in papers)
    2. 'web' (Recent trends, broad tech context, or breaking news)
    3. 'hybrid' (Both layers needed)
    Respond strictly in JSON format matching: {{"route": "local" | "web" | "hybrid"}}'''
    
    response = await llm_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    decision = json.loads(response.choices[0].message.content).get("route", "hybrid")
    return {"route_decision": decision}

async def local_rag_node(state: AgentState) -> dict:
    """Performs retrieval embedding transformation and vector DB parsing."""
    # Production note: In reality, call your embedding service (e.g., OpenAI text-embedding-3-large) first
    # This mock vector assumes match configuration size 1024
    mock_query_vector = [0.1] * 1024 
    
    raw_docs = await db.semantic_search(query_vector=mock_query_vector, top_k=6)
    reranked_docs = cross_encoder_rerank(state["query"], raw_docs, keep_top_n=3)
    return {"retrieved_documents": reranked_docs}

async def web_search_node(state: AgentState) -> dict:
    """Queries public infrastructure APIs for contextual external augmentations."""
    results = await web_search_tool(query=state["query"])
    return {"web_results": results}

async def synthesis_generation_node(state: AgentState) -> dict:
    """Assembles all variable dynamic contexts to execute clean, structured generation."""
    context_str = ""
    if state.get("retrieved_documents"):
        context_str += "\n[Local Literature Chunks]:\n" + "\n".join(
            [f"Doc: {d['metadata']['title']} (Page {d['metadata']['page']}): {d['text']}" for d in state["retrieved_documents"]]
        )
    if state.get("web_results"):
        context_str += "\n[Web Search Context]:\n" + "\n".join(
            [f"Source: {w['title']} ({w['url']}): {w['content']}" for w in state["web_results"]]
        )

    prompt = f"""Using ONLY the compiled context below, answer the user query. 
    You must cite sources inline using Markdown format matching either [Title, Page X] or [Source Title](URL).
    
    Context:
    {context_str}
    
    Query: {state['query']}"""

    response = await llm_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"generation": response.choices[0].message.content}

def router_edge_logic(state: AgentState):
    """Evaluates router node string outcomes to emit execution path targets."""
    decision = state["route_decision"]
    if decision == "local":
        return "local_rag"
    elif decision == "web":
        return "web_search"
    return "hybrid_path"

# Structural Construction of the StateGraph Layout Map
workflow = StateGraph(AgentState)

# Append Working Module Nodes
workflow.add_node("intent_router", routing_node)
workflow.add_node("local_rag", local_rag_node)
workflow.add_node("web_search", web_search_node)
workflow.add_node("synthesis_generator", synthesis_generation_node)

# Map Explicit Flow Edges
workflow.set_entry_point("intent_router")

workflow.add_conditional_edges(
    "intent_router",
    router_edge_logic,
    {
        "local_rag": "local_rag",
        "web_search": "web_search",
        "hybrid_path": "local_rag" # In simple DAG layout, we branch sequentially or in parallel
    }
)

# Connect tracking convergence targets
workflow.add_edge("local_rag", "synthesis_generator")
workflow.add_edge("web_search", "synthesis_generator")
workflow.add_edge("synthesis_generator", END)

# Compile engine run object
runtime_agent = workflow.compile()
