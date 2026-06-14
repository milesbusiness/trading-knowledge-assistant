# Development Guide

## Prerequisites

- Python 3.12
- Azure AI Search (Standard)
- Azure OpenAI (GPT-4o + text-embedding-3-large)
- Azure Storage Account (optional — blob upload degrades gracefully)

## Setup

```bash
git clone https://github.com/milesbusiness/trading-knowledge-assistant
cd trading-knowledge-assistant

python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

cp .env.example .env
# Fill in Azure credentials in .env
```

## Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
# Swagger UI: http://localhost:8080/docs
```

## Try It

```bash
# Upload a document
curl -X POST http://localhost:8080/api/documents \
  -F "file=@mifid2-rts.pdf"

# Ask a question
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the transaction reporting obligation under MiFID II?", "session_id": "analyst-1"}'

# Follow-up (uses session memory)
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the deadlines?", "session_id": "analyst-1"}'
```

## Project Structure

```
trading-knowledge-assistant/
├── app/
│   ├── main.py                    ← FastAPI app + lifespan
│   ├── api/routes/
│   │   ├── chat.py                ← POST /api/chat
│   │   └── documents.py           ← POST/GET/DELETE /api/documents
│   └── core/
│       ├── config.py              ← pydantic-settings (reads .env)
│       ├── azure_search.py        ← index creation on startup
│       ├── rag_pipeline.py        ← LangChain RAG + session memory
│       └── document_ingestion.py  ← chunk → embed → index
├── docs/
│   ├── ARCHITECTURE.md
│   └── DEVELOPMENT.md
├── requirements.txt
├── Dockerfile
└── .env.example
```

## Docker

```bash
docker build -t trading-knowledge-assistant .
docker run -p 8080:8080 --env-file .env trading-knowledge-assistant
```
