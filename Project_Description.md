Here is a professional, high-density GitHub project description. It is structured to mirror the exact format tech recruiters and engineering managers look for: focusing on architecture, engineering challenges, and business value rather than basic tutorials.
------------------------------
## Agentic-RAG-Researcher: Hybrid Context Question-Answering System with Web Search & Precise Citations
A production-grade, stateful Agentic-RAG pipeline designed for researchers and students to query academic literature. The system intelligently routes queries between an internal vector store of parsed research papers and live internet search, employing advanced reranking and structured metadata parsing to deliver factual answers with verifiable inline citations.
## 🚀 Key Architectural Features

* Intent-Based Query Routing: Utilizes an LLM-based router to classify user queries and dynamically branch execution between Local RAG (vector database) and Web RAG (search APIs) based on context freshness and availability.
* Structure-Aware PDF Parsing: Bypasses naive text extraction by using layout-aware parsing (LlamaParse/Marker) to properly preserve multi-column formatting, tables, and mathematical notations from scientific PDFs.
* Hierarchical Chunking & Reranking: Implements parent-child document chunking to preserve global context during indexing. Uses a cross-encoder (BGE-Reranker-Large) to prune irrelevant context blocks, reducing LLM context window bloat and context-stuffing costs.
* Deterministic Citation Mapping: Enforces strict inline metadata binding. Every generated response includes markdown links linked back to exact document chunks containing specific metadata (Title, Authors, Page Number, DOI) or web URLs.
* Asynchronous Agentic Orchestration: Built on top of LangGraph as a stateful, cyclic agent, enabling graceful error-handling, query rewriting when retrieval yield is low, and token streaming.

## 🛠️ Tech Stack

* LLM Orchestration: LangGraph / FastAPI
* Vector Database: Qdrant (Self-hosted via Docker)
* Embeddings & Reranking: Hugging Face Transformers (BAAI/bge-large-en-v1.5), Cohere API
* Web Retrieval: Tavily API / Brave Search API
* Evaluation Framework: Ragas (Monitoring Context Precision, Faithfulness, and Answer Relevance)
* Deployment: Docker, Streamlit (Frontend), GitHub Actions (CI/CD)

## 📊 Evaluation & Performance Metrics
(Tip: Fill these numbers in with your actual benchmark results once you run your evaluation script!)

* Faithfulness Rate: Achieved 0.XX score via Ragas, minimizing hallucinations by applying automated strict-context prompt engineering.
* Latency Optimization: Reduced time-to-first-token (TTFT) by XX% using async streaming endpoints and optimizing vector query payloads.
* Retrieval Efficiency: Reranking improved Context Recall by XX% compared to naive top-k cosine similarity retrieval.

------------------------------
Would you like me to generate the System Architecture Diagram in text format (Mermaid code) so you can render a visual flowchart directly inside this GitHub README?

