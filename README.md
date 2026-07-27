# Routing-and-Agentic-RAG

That is an excellent project choice for a Machine Learning Engineer portfolio. Building an hybrid system that combines local documentation (RAG) with real-time web data (Web Search / RAG) is highly relevant to what companies are actively building right now. [1, 2, 3] 
To make this stand out to a hiring manager, you need to treat it as an engineering problem, not just a wrapper script. Here is how to architect this system to maximize its impact on your portfolio: [4] 
## 1. Advanced Architecture Strategy
Do not just use standard LangChain or LlamaIndex defaults. Instead, implement a Routing and Agentic RAG architecture: [5] 

* The Intent Router: When a user asks a question, use a lightweight model (or a semantic router like Semantic Router) to decide:
1. Is the answer purely inside the uploaded papers? (Route to Vector DB).
   2. Does it require external context or newer data? (Route to Web Search).
   3. Does it require both? (Route to a Hybrid Agent). [6, 7, 8, 9, 10] 
* The Search Component: Integrate an API like Tavily, SearxNG, or Brave Search to fetch real-time web results when the local database falls short.

## 2. Concrete Production Stack
Using this specific stack will show recruiters you know the industry-standard tools:

* Ingestion & Parsing: Marker or LlamaParse (Standard PDF parsers fail heavily on research paper columns, tables, and mathematical formulas).
* Vector Database: Qdrant or Milvus (Running locally in a Docker container to show database management skills).
* Orchestration: LangGraph or LlamaIndex Workflows (Stateful, asynchronous control flows handle complex agent logic better than basic chains).
* Serving API: FastAPI with streaming enabled (EventSourceResponse). [11, 12, 13, 14, 15] 

## 3. Key MLE Features to Implement (The "Selling Points")
These engineering details are what will separate you from junior candidates:

* Hierarchical Node Parsing: Research papers have a structure (Abstract, Methods, Results). Implement parent-child chunking where small chunks are used for semantic retrieval, but the larger parent section context is fed to the LLM. [16, 17, 18, 19, 20] 
* Precise Citation Mechanism: Store the PDF metadata strictly (Title, Authors, Page Number, DOI). When generating an answer, prompt the LLM to output inline markdown citations [1], and map those exactly to the metadata keys in your frontend. [21] 
* Reranking Step: Before sending retrieved chunks to the LLM, pass them through a cross-encoder reranker like BGE-Reranker-Large or Cohere Reranker to filter out irrelevant search or vector results. [22, 23, 24, 25, 26] 

## 4. MLOps & Evaluation (Crucial for MLE Roles)
An engineer must prove their system works reliably. Dedicate a section of your repository to evaluation:

* Use Ragas or TruLens to measure and log your system's performance on three core metrics:
1. Faithfulness: Is the LLM hallucinating, or relying strictly on the papers/web results?
   2. Answer Relevance: Does the response actually answer the user's prompt?
   3. Context Precision: Did your retrieval pipeline actually fetch the right chunks? [27, 28, 29] 

To help tailor the next steps for your project plan, could you share:

* Will you be deploying this using open-source local models (like Llama 3 running via Ollama/vLLM) or commercial APIs (like OpenAI or Anthropic)?
* What is your target timeline to complete this portfolio project?


[1] [https://byteridge.com](https://byteridge.com/technology-trends/understanding-retrieval-augmented-generation-rag/)
[2] [https://arxiv.org](https://arxiv.org/html/2501.09136v1)
[3] [https://link.springer.com](https://link.springer.com/article/10.1007/s11044-026-10164-7)
[4] [https://www.linkedin.com](https://www.linkedin.com/pulse/rag-explained-simply-retrieval-augmented-generation-real-humans-7punc)
[5] [https://www.linkedin.com](https://www.linkedin.com/posts/brijpandeyji_your-team-picked-a-rag-pattern-6-months-ago-activity-7443270919613095936-o2Fx)
[6] [https://arxiv.org](https://arxiv.org/html/2405.06683v1)
[7] [https://arxiv.org](https://arxiv.org/html/2312.10997v5)
[8] [https://www.gocloud7.com](https://www.gocloud7.com/smarter-query-handling-multi-level-prompting-in-a-rag-based-chatbot-part-3/)
[9] [https://www.instaclustr.com](https://www.instaclustr.com/education/retrieval-augmented-generation/graph-rag-vs-vector-rag-3-differences-pros-and-cons-and-how-to-choose/)
[10] [https://medium.com](https://medium.com/@ankur0x/step-by-step-tutorial-build-a-rag-based-pdf-assistant-with-langchain-and-groq-cb05d2c1b538)
[11] [https://jamwithai.substack.com](https://jamwithai.substack.com/p/bringing-your-rag-system-to-life)
[12] [https://medium.com](https://medium.com/the-ai-forum/rag-on-complex-pdf-using-llamaparse-langchain-and-groq-5b132bd1f9f3)
[13] [https://www.firecrawl.dev](https://www.firecrawl.dev/glossary/web-extraction-apis/pdf-to-rag-ready-data)
[14] [https://qdrant.tech](https://qdrant.tech/documentation/tutorials-build-essentials/rag-deepseek/)
[15] [https://medium.com](https://medium.com/vector-database/building-an-intelligent-video-deduplication-system-powered-by-vector-similarity-search-5dca46801313)
[16] [https://ondezx.com](https://ondezx.com/blog/machine-learning-research-paper)
[17] [https://dl.acm.org](https://dl.acm.org/doi/fullHtml/10.1145/3654522.3654557)
[18] [https://www.researchprospect.com](https://www.researchprospect.com/research-paper-methodology/)
[19] [https://www.designveloper.com](https://www.designveloper.com/blog/advanced-rag/)
[20] [https://diptendud.medium.com](https://diptendud.medium.com/top-30-gen-ai-rag-interview-questions-b9453c6ff06f)
[21] [https://apxml.com](https://apxml.com/courses/getting-started-rag/chapter-4-rag-generation-augmentation/attributing-sources)
[22] [https://towardsdatascience.com](https://towardsdatascience.com/rag-explained-reranking-for-better-answers/)
[23] [https://www.chitika.com](https://www.chitika.com/best-open-source-re-ranker-rag/)
[24] [https://arxiv.org](https://arxiv.org/html/2508.09755v1)
[25] [https://www.reddit.com](https://www.reddit.com/r/Rag/comments/1ls6e3r/whats_the_best_rag_tech_stack_these_days_from/)
[26] [https://fast.io](https://fast.io/resources/rag-with-large-files/)
[27] [https://medium.com](https://medium.com/@siraj_raval/architecting-trustworthy-rag-a-deep-dive-into-hybrid-search-reranking-pii-redaction-and-7e98976e1985)
[28] [https://ijctece.com](https://ijctece.com/index.php/IJCTEC/article/download/170/132)
[29] [https://www.instagram.com](https://www.instagram.com/reel/DamUcpfxjE3/)
