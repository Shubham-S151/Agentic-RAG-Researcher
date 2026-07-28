## The Goal

Let's build a project that feels like something an engineer at OpenAI, Anthropic, Microsoft, Databricks, Snowflake, or a GenAI startup would write.

Not just:

> "I built a RAG chatbot."

Instead:

> "I designed a modular, production-grade Agentic RAG system with routing, hybrid retrieval, reranking, evaluation, streaming APIs, and structured citations."

That's a much stronger portfolio story.

---

# Project Vision

We'll build a **production-grade Hybrid Agentic RAG system**.

The pipeline will look like this:

```text
                 User Query
                      │
                      ▼
            Intent Router (Semantic)
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
   Local RAG       Web Search      Hybrid Route
      │               │                │
      └───────────────┴────────────────┘
                      ▼
             Merge Retrieved Docs
                      ▼
             Cross Encoder Reranker
                      ▼
         Retrieval Quality Checker
          │                    │
          ▼                    ▼
      Enough?           Rewrite Query
          │                    │
          └────────────┬───────┘
                       ▼
              Context Builder
                       ▼
             Grounded LLM Generation
                       ▼
          Structured Citation Mapping
                       ▼
          Hallucination Verification
                       ▼
              Streaming API Response
```

---

# Tech Stack

I recommend the following stack.

## Backend

* Python 3.12
* FastAPI
* LangGraph
* Pydantic v2
* asyncio
* uvicorn

---

## Vector Database

* Qdrant
* Docker Compose

---

## Embeddings

Choose one:

Local

* BAAI/bge-large-en-v1.5

or

API

* OpenAI text-embedding-3-large

I'd recommend **starting with OpenAI embeddings** because they simplify development. Once everything works, you can swap in a local embedding model.

---

## LLM

Start with

* GPT-4.1 or GPT-4o

Later add

* Ollama
* vLLM
* LiteLLM provider abstraction

---

## Search

Start with

* Tavily

Later support

* Brave
* SearxNG

---

## Reranker

* BAAI/bge-reranker-large

---

## Evaluation

* Ragas

---

## Frontend

* Streamlit

---

## Deployment

* Docker Compose
* GitHub Actions

---

# Folder Structure

This is the structure I'd recommend:

```text
agentic-rag-researcher/

src/

    api/
        app.py
        routes.py
        schemas.py
        dependencies.py
        middleware.py

    config/
        settings.py
        logging.py

    graph/
        graph.py
        state.py
        nodes.py
        edges.py

    ingestion/
        parser.py
        metadata.py
        chunking.py
        embeddings.py
        indexer.py

    retrieval/
        vector_store.py
        retriever.py
        hybrid.py
        reranker.py
        citations.py

    search/
        base.py
        tavily.py
        brave.py

    models/
        llm.py
        embeddings.py

    prompts/
        router.py
        generator.py
        verifier.py

    evaluation/
        ragas_eval.py

    utils/
        timers.py
        cache.py
        exceptions.py

tests/

docker/

streamlit/

scripts/

README.md
```

This organization separates concerns clearly and makes future extensions straightforward.

---

# Development Roadmap

I recommend building it in phases so that every stage results in a working system.

### Phase 1 – Infrastructure

Focus on the project skeleton and configuration.

Deliverables:

* FastAPI application
* Configuration management
* Logging
* Docker Compose with Qdrant
* Health endpoints

---

### Phase 2 – Document Ingestion

Implement:

* PDF parsing
* Metadata extraction
* Hierarchical chunking
* Embeddings
* Qdrant indexing

At the end of this phase, you'll have a searchable vector database.

---

### Phase 3 – Retrieval

Implement:

* Dense retrieval
* Metadata filtering
* Parent-child retrieval
* Configurable retrieval parameters

---

### Phase 4 – Reranking

Implement:

* BGE reranker
* Batched inference
* Top-k pruning

---

### Phase 5 – Search

Implement:

* Tavily integration
* Retry logic
* Result normalization
* Caching

---

### Phase 6 – LangGraph

Implement:

* Router node
* Retrieval nodes
* Merge node
* Generation node
* Verification node
* Retry loop

---

### Phase 7 – Streaming

Implement:

* Streaming responses
* Structured citations
* Token streaming

---

### Phase 8 – Evaluation

Implement:

* Ragas evaluation
* Benchmark scripts
* Metrics dashboard

---

# Repository Timeline

Build the project in this order:

1. Repository setup
2. Configuration
3. API
4. Vector database
5. Embeddings
6. Ingestion
7. Retrieval
8. Search
9. Reranking
10. LangGraph
11. Prompt management
12. Evaluation
13. Frontend
14. Docker
15. CI/CD
16. Documentation

Each milestone leaves you with a functioning, testable system.

---

# What We'll Improve Compared to the Current Version

The rebuilt project will address the gaps we identified:

* Replace mock embeddings with a real embedding service.
* Build a true hybrid retrieval path that combines local and web results.
* Introduce structured citation objects instead of relying on markdown generation.
* Add query rewriting and verification loops to the LangGraph workflow.
* Centralize configuration, logging, and dependency management.
* Add proper error handling, retries, and graceful degradation.
* Support streaming responses and evaluation out of the box.

---

## How I Suggest We Work

Rather than rewriting isolated files, we'll build the project **module by module**. That keeps the architecture coherent and avoids accumulating technical debt.

The order I'd use is:

1. Project directory structure
2. `pyproject.toml` and dependency management
3. `config/settings.py`
4. Logging infrastructure
5. FastAPI application and dependency injection
6. Pydantic schemas
7. Qdrant vector store
8. Embedding service
9. PDF ingestion pipeline
10. Retrieval and reranking
11. Web search abstraction
12. LangGraph state, nodes, and graph
13. Streamlit frontend
14. Docker, testing, evaluation, and CI

By the end, you'll have a repository that not only works but also demonstrates software engineering practices expected in production AI systems.
