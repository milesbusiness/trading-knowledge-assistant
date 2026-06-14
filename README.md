# Trading Knowledge Assistant

> Python + FastAPI + LangChain RAG assistant for trading domain knowledge, deployed on Azure Kubernetes Service.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C)](https://langchain.com)
[![Azure AI Search](https://img.shields.io/badge/Azure_AI_Search-hybrid-0089D6?logo=microsoft-azure)](https://azure.microsoft.com/products/ai-services/ai-search)

---

## What It Does

An internal RAG assistant for trading desks — answers domain questions using an indexed knowledge base of trading playbooks, market structure docs, and regulatory guidance.

- Upload documents (PDF, Markdown, text)
- Ask questions in natural language with streamed answers
- Hybrid semantic + keyword search (Azure AI Search)
- Source citations with page references
- Multi-turn conversation with session memory
- Async FastAPI — handles concurrent analyst queries

---

## Architecture

```
Client
  │
  ▼
FastAPI (port 8080)
  ├── POST /api/chat         ← LangChain RAG chain with ConversationBufferMemory
  ├── POST /api/documents    ← Ingestion pipeline
  ├── GET  /api/documents    ← List indexed documents
  └── GET  /health

LangChain Pipeline:
  Question
    → AzureAISearchRetriever (hybrid search, top-5)
    → StuffDocumentsChain
    → AzureChatOpenAI (GPT-4o)
    → Answer + sources
```

---

## Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Fill in Azure credentials

# 3. Run
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# 4. Try
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the best execution policy for equity trades?", "session_id": "analyst-1"}'
```

---

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Ask a question (returns answer + sources) |
| `POST` | `/api/documents` | Upload and ingest a document |
| `GET`  | `/api/documents` | List all indexed documents |
| `DELETE` | `/api/documents/{id}` | Remove document |
| `GET`  | `/health` | Health check |

---

## Deployment (AKS)

```bash
docker build -t ghcr.io/milesbusiness/trading-knowledge-assistant:latest .
docker push ghcr.io/milesbusiness/trading-knowledge-assistant:latest
kubectl apply -f k8s/
```

---

## License

MIT
