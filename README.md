# Trading Knowledge Assistant

> **Conversational AI that gives trading desk analysts instant, multi-turn answers from your firm's internal knowledge base — playbooks, regulatory guidance, strategy documentation.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C)](https://langchain.com)
[![Azure AI Search](https://img.shields.io/badge/Azure_AI_Search-Standard-0089D6?logo=microsoft-azure)](https://azure.microsoft.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## The Problem

Every trading desk accumulates institutional knowledge in the heads of experienced people, buried in shared drives, or scattered across documents nobody can find. When a senior analyst leaves, that knowledge walks out the door. When a new analyst joins, they spend months asking questions that hundreds of colleagues have asked before.

More critically: in a fast-moving market, an analyst needing to recall the firm's hedging playbook cannot spend 20 minutes searching SharePoint. They need the answer now.

**The result:** Slow onboarding, repeated knowledge transfer effort, and decision-making delays at exactly the moments when speed matters most.

## The Solution

A conversational AI system built on your firm's internal documents. Analysts ask questions in plain English and receive instant, accurate answers drawn from your actual playbooks and policies. The system remembers the last 10 messages — enabling natural multi-turn conversations without repeating context, exactly like talking to a knowledgeable colleague.

---

## Conversation Example

```
Analyst:    "What is our hedging policy for FX exposure above 10 million EUR?"
Assistant:  "According to the FX Risk Management Playbook (Section 4.2), exposures
             above EUR 10M require mandatory hedging within T+2 using approved
             instruments: FX forwards, vanilla options, or NDF for restricted
             currencies. Approval from the Head of Trading is required for
             exposures above EUR 50M. [Source: FX-Playbook-2024.pdf, p.18]"

Analyst:    "What instruments are approved for restricted currencies?"
Assistant:  "For restricted currencies, the approved instruments are Non-Deliverable
             Forwards (NDFs) and cash-settled options. The list of restricted
             currencies includes CNY, INR, BRL, KRW, and TWD. Physical delivery
             forwards are not permitted for these currencies. [Source: FX-Playbook-2024.pdf, p.22]"

Analyst:    "And what is the maximum tenor?"
Assistant:  "For restricted currency NDFs, the maximum tenor is 12 months. For
             developed market currencies, the maximum tenor for hedging instruments
             is 24 months without senior approval. [Source: FX-Playbook-2024.pdf, p.23]"
```

The system correctly used the prior conversation context — understanding that "restricted currencies" referred to the ones mentioned in the previous answer, and "maximum tenor" referred to the hedging instruments being discussed.

---

## Key Capabilities

### Conversational Memory (10-Turn Window)
Each analyst session maintains a sliding window of the last 10 conversation turns. Follow-up questions are understood in context — no need to repeat what you just said.

### Hybrid Document Search
Combines BM25 keyword search (precise for exact terms, ticker symbols, article references) with vector semantic search (precise for conceptual questions). The dual approach significantly outperforms either method alone.

### Multi-Document Knowledge Base
Supports any number of internal documents — playbooks, regulatory summaries, strategy guides, risk frameworks, onboarding materials. New documents can be added at any time via the API.

### Category Filtering
Documents are automatically categorised as regulatory, strategy, risk, or general. Analysts can filter queries to a specific category for more targeted results.

### Source Citations
Every answer includes the document name, page number, and the specific text used. Analysts can verify responses against the source document.

### Session Isolation
Each analyst session is independently managed. Multiple analysts can use the system simultaneously with separate conversation histories.

---

## How It Works

```
Internal Documents (PDF, Word, text)
         │
         ▼
Document Ingestion Pipeline
  ├── Upload to Azure Blob (archive)
  ├── Split into 1,000-token chunks (100 overlap)
  ├── Embed with text-embedding-3-large (1536 dimensions)
  └── Index in Azure AI Search (keyword + vector + semantic)
         │
         ▼
Analyst sends message (with session_id)
         │
         ▼
LangChain ConversationalRetrievalChain
  ├── Load session memory (last 10 turns)
  ├── Reformulate question with history context
  ├── Hybrid search (keyword + vector + reranker)
  ├── Retrieve top-5 most relevant chunks
  ├── Build prompt: system + memory + chunks + question
  └── GPT-4o generates cited answer
         │
         ▼
Response stored in session memory
         │
         ▼
Answer + citations returned to analyst
```

---

## API Reference

### Chat (Multi-Turn Conversation)
```http
POST /api/chat
Content-Type: application/json

{
  "message": "What is our delta hedging procedure for equity options positions?",
  "session_id": "analyst-dilip-session-1"
}
```

**Response:**
```json
{
  "answer": "According to the Equity Derivatives Risk Manual (Section 6), delta hedging for options positions must be executed within 30 minutes of position entry...",
  "citations": [
    {
      "document": "Equity-Derivatives-Risk-Manual-2024.pdf",
      "page": 34,
      "excerpt": "Delta hedging shall be executed within 30 minutes..."
    }
  ],
  "session_id": "analyst-dilip-session-1",
  "turn": 1
}
```

### Upload Document
```http
POST /api/documents
Content-Type: multipart/form-data

file: [PDF or text file]
category: "strategy"   # optional: regulatory / strategy / risk / general
```

### List Documents
```http
GET /api/documents
```

### Delete Document
```http
DELETE /api/documents/{document_id}
```

---

## Technology Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| API Framework | Python FastAPI | Async, high-performance, automatic OpenAPI docs |
| AI Orchestration | LangChain 0.3 | ConversationalRetrievalChain, native Azure Search integration |
| Conversation Memory | ConversationBufferWindowMemory (k=10) | Sliding window, prevents context overflow |
| Language Model | Azure OpenAI GPT-4o | Answer generation with citation awareness |
| Embedding Model | Azure OpenAI text-embedding-3-large | State-of-the-art semantic embeddings (1536d) |
| Vector Search | Azure AI Search (HNSW algorithm) | Sub-100ms approximate nearest neighbour |
| Document Storage | Azure Blob Storage | Immutable document archive |
| Deployment | Docker + Azure Container Apps | Containerised, auto-scaling |

---

## Business Value

| Metric | Before | After |
|--------|--------|-------|
| Time to find a specific policy | 15–30 minutes | < 10 seconds |
| New analyst onboarding duration | 3–6 months | 2–4 weeks |
| Senior analyst time on Q&A | 30–60 min/day | Near zero |
| Knowledge retention when people leave | Lost | Preserved in document index |
| Consistency of answers across the desk | Variable | Consistent (single source) |

---

## Getting Started

### Prerequisites
- Python 3.12
- Azure AI Search (Standard)
- Azure OpenAI (GPT-4o + text-embedding-3-large)

### Setup
```bash
git clone https://github.com/milesbusiness/trading-knowledge-assistant
cd trading-knowledge-assistant

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Fill in Azure credentials in .env
```

### Run
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
# Docs: http://localhost:8080/docs
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [Executive Summary](docs/EXECUTIVE_SUMMARY.md) | Business case, onboarding ROI, stakeholder guide |
| [Architecture Guide](docs/ARCHITECTURE.md) | LangChain chain design, memory model, hybrid search |
| [Development Guide](docs/DEVELOPMENT.md) | Setup, configuration, adding documents |

---

## About

Built to demonstrate Python-based conversational RAG architecture for financial services knowledge management, targeting Principal Architect and AI Solution Architect roles at European financial institutions.

**Author:** Dilip Kumar Jena | **Framework:** LangChain + FastAPI | **Platform:** Azure
