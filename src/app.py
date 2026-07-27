from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.graph import runtime_agent
from src.database import QdrantVectorStore

app = FastAPI(title="Agentic-RAG Researcher Infrastructure API", version="1.0.0")
db_client = QdrantVectorStore()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    route_taken: str
    answer: str

@app.on_event("startup")
async def startup_event():
    """Trigger vector connection layers safely during environment scaling initialization."""
    await db_client.initialize_collection()

@app.post("/api/v1/query", response_model=QueryResponse)
async def execute_agent_query(payload: QueryRequest):
    try:
        # Construct type-conforming initial input dictionary map
        initial_state = {
            "query": payload.query,
            "route_decision": "",
            "retrieved_documents": [],
            "web_results": [],
            "compiled_context": "",
            "generation": "",
            "citation_mappings": [],
            "retry_count": 0,
            "is_hallucination": False
        }
        
        # Stream or resolve async state graph transitions to terminal output configuration blocks
        output_state = await runtime_agent.ainvoke(initial_state)
        
        return QueryResponse(
            query=output_state["query"],
            route_taken=output_state["route_decision"],
            answer=output_state["generation"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine runtime error execution: {str(e)}")
