# Trading Knowledge Assistant — Architecture

## Overview

A RAG assistant that gives trading desk analysts instant answers from an internal knowledge base — playbooks, regulatory guidance, market structure docs. Built on LangChain + FastAPI + Azure AI Search.

---

## Architecture

```
Client (browser / curl)
        │
        ▼
FastAPI (port 8080)
  ├── POST /api/chat          ← conversational RAG with session memory
  └── POST /api/documents     ← ingest pipeline

        │
        ▼ (chat route)
LangChain ConversationalRetrievalChain
  ├── AzureAISearchRetriever
  │     ├── hybrid search (keyword + vector)
  │     ├── semantic reranking
  │     └── top-5 chunks returned
  │
  ├── StuffDocumentsChain
  │     └── assembles context + chat history + question → prompt
  │
  └── AzureChatOpenAI (GPT-4o)
        └── generates answer with source citations

        │
        ▼ (ingestion route)
Document Ingestion Pipeline
  ├── BlobServiceClient     → upload to Azure Blob
  ├── AzureOpenAIEmbeddings → embed chunks (text-embedding-3-large)
  └── SearchClient          → upload to Azure AI Search index
```

---

## Session Memory

Each `session_id` gets its own `ConversationBufferWindowMemory(k=10)` — the last 10 turns are included in every request. This enables multi-turn conversations:

```
Analyst: "What is best execution under MiFID II?"
→ [answer about Art. 27]

Analyst: "And how does it apply to algorithmic trading?"
→ LangChain includes previous Q&A in context → coherent follow-up answer
```

Sessions are in-memory (reset on restart). For persistence, replace with Redis-backed memory.

---

## Azure AI Search Index Schema

```python
fields = [
    SimpleField("id", key=True, filterable=True),
    SimpleField("document_id", filterable=True),
    SearchableField("document_name", filterable=True),
    SearchableField("content", analyzer_name="en.microsoft"),   # keyword
    SimpleField("page_number", filterable=True),
    SimpleField("category", filterable=True, facetable=True),   # regulatory/strategy/risk
    SearchField("content_vector",                               # vector
        type=Collection(Single),
        vector_search_dimensions=1536,
        vector_search_profile_name="hnsw-profile")
]
```

Search type: `"hybrid"` — BM25 + cosine similarity + semantic reranker.

---

## Hybrid Search vs Pure Vector

| Approach | Pros | Cons |
|----------|------|------|
| Pure keyword (BM25) | Exact term match | Misses paraphrases |
| Pure vector | Semantic similarity | Misses exact article refs |
| **Hybrid** | Best of both | Slightly higher latency |

For trading documents: exact regulation article references (`"Art. 26"`, `"EMIR"`) need keyword precision. Conceptual questions (`"what is best execution"`) need semantic similarity. Hybrid wins on both.

---

## Key Design Decisions

### LangChain over Semantic Kernel
Python ecosystem has more mature Azure AI Search + LangChain integrations (native `AzureSearch` vector store class). Semantic Kernel is preferred for C# services.

### FastAPI + async
All I/O operations (blob upload, search, OpenAI) are awaited. FastAPI handles concurrent analyst queries without blocking.

### Category auto-detection
Documents are automatically categorised (`regulatory` / `strategy` / `risk` / `general`) based on keyword presence. Enables filtered searches: `GET /api/chat?category=regulatory`.

---

## References

### LangChain
- [LangChain docs — ConversationalRetrievalChain](https://python.langchain.com/docs/use_cases/question_answering/chat_history)
- [LangChain docs — Memory](https://python.langchain.com/docs/modules/memory/)
- [YouTube: LangChain RAG Tutorial (Fireship, 10 min)](https://www.youtube.com/watch?v=tcqEUSNCn8I)
- [YouTube: Advanced RAG techniques (LlamaIndex / LangChain deep dive, 1h)](https://www.youtube.com/watch?v=TRjq7t2Ms5I)

### Azure AI Search (Python)
- [Azure AI Search Python SDK](https://learn.microsoft.com/en-us/python/api/overview/azure/search-documents-readme)
- [LangChain AzureSearch vector store](https://python.langchain.com/docs/integrations/vectorstores/azuresearch)

### FastAPI
- [FastAPI docs](https://fastapi.tiangolo.com/)
- [FastAPI async best practices](https://fastapi.tiangolo.com/async/)
- [YouTube: FastAPI full course (freeCodeCamp, 6h)](https://www.youtube.com/watch?v=0sOvCWFmrtA)

### RAG Design Patterns
- [RAG survey paper — Retrieval-Augmented Generation for NLP (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401)
- [YouTube: RAG from scratch (LangChain official playlist)](https://www.youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x)
