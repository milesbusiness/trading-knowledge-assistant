# Technical Guide — Trading Knowledge Assistant

> This guide explains every technology used, how to learn it, how to install the project, what every file does, and how to see the output.

---

## Table of Contents

1. [Technologies Used](#1-technologies-used)
2. [Where to Learn Each Technology](#2-where-to-learn-each-technology)
3. [Installation — Step by Step](#3-installation--step-by-step)
4. [Project File Structure](#4-project-file-structure)
5. [Code Walkthrough — Every File Explained](#5-code-walkthrough--every-file-explained)
6. [How to Run and View Output](#6-how-to-run-and-view-output)

---

## 1. Technologies Used

| Technology | Version | What it is | Why it is used here |
|-----------|---------|-----------|-------------------|
| **Python** | 3.12 | General-purpose programming language | The entire application is Python |
| **FastAPI** | 0.115.5 | Modern Python web framework | Exposes the REST API; auto-generates `/docs` (Swagger UI) |
| **Uvicorn** | 0.32.1 | ASGI server for Python | Runs the FastAPI application; handles async HTTP connections |
| **Pydantic** | 2.10.3 | Data validation library for Python | Validates request/response bodies; auto-generates OpenAPI schema |
| **LangChain** | 0.3.9 | Python AI orchestration framework | Provides `ConversationalRetrievalChain` — the core RAG pipeline |
| **langchain-openai** | 0.2.11 | LangChain connector for OpenAI/Azure OpenAI | `AzureChatOpenAI` and `AzureOpenAIEmbeddings` classes |
| **langchain-community** | 0.3.9 | LangChain community integrations | `AzureSearch` vector store integration |
| **Azure AI Search** | 11.6.0 (SDK) | Microsoft's cloud search service | Stores document embeddings; performs hybrid BM25 + vector search |
| **Azure Blob Storage** | 12.21.0 (SDK) | Microsoft's cloud object storage | Archives the original uploaded documents |
| **Azure OpenAI GPT-4o** | — | Microsoft-hosted GPT-4o | Generates the final answer from retrieved document chunks |
| **text-embedding-3-large** | — | Azure OpenAI embedding model | Converts text to 1536-dimensional vectors for semantic search |
| **ConversationalRetrievalChain** | LangChain | Pre-built chain combining retrieval + conversation | Handles context reformulation and memory automatically |
| **ConversationBufferWindowMemory** | LangChain | Sliding window conversation memory | Remembers the last 10 turns of conversation per session |
| **Docker** | — | Container runtime | Packages the app for deployment to Azure Container Apps |

**Official Links:**
- FastAPI: https://fastapi.tiangolo.com/
- LangChain: https://python.langchain.com/docs/introduction
- LangChain GitHub: https://github.com/langchain-ai/langchain
- Azure AI Search Python SDK: https://learn.microsoft.com/azure/search/search-howto-dotnet-sdk
- Azure Blob Storage Python SDK: https://learn.microsoft.com/azure/storage/blobs/storage-quickstart-blobs-python
- Azure OpenAI: https://learn.microsoft.com/azure/ai-services/openai/overview

---

## 2. Where to Learn Each Technology

### Python 3.12

**Official:**
- https://docs.python.org/3.12/ — Full documentation
- https://docs.python.org/3/tutorial/ — Tutorial (start here)

**YouTube:**
- "Python Tutorial for Beginners" by Mosh Hamedani — https://www.youtube.com/@programmingwithmosh
- "Python for Data Science" by freeCodeCamp — https://www.youtube.com/@freecodecamp

**What to focus on:** async/await, type hints (`str | None`), dataclasses, f-strings

### FastAPI

**Official:**
- https://fastapi.tiangolo.com/tutorial/ — Full tutorial (excellent, very clear)
- https://fastapi.tiangolo.com/async/ — Async explanation

**YouTube:**
- "FastAPI Tutorial" by Tech With Tim — https://www.youtube.com/@TechWithTim
- "FastAPI full course" by Sanjeev Thiyagarajan — search on YouTube

**What to focus on:** `@app.post`, `BaseModel`, `APIRouter`, lifespan events

### LangChain

**Official:**
- https://python.langchain.com/docs/tutorials/rag — RAG tutorial (most relevant to this project)
- https://python.langchain.com/docs/concepts/memory — Memory concepts
- https://python.langchain.com/docs/integrations/vectorstores/azuresearch — Azure AI Search integration

**YouTube:**
- "LangChain Crash Course" by Greg Kamradt — https://www.youtube.com/@DataIndependent
- "RAG from scratch" by LangChain — https://www.youtube.com/@LangChain

**What to focus on:** `ConversationalRetrievalChain`, `ConversationBufferWindowMemory`, `AzureSearch` vector store

### Azure AI Search

**Official:**
- https://learn.microsoft.com/azure/search/search-what-is-azure-search — What it is
- https://learn.microsoft.com/azure/search/search-get-started-vector — Vector search quickstart
- https://learn.microsoft.com/azure/search/hybrid-search-overview — Hybrid search overview (BM25 + vector)

**YouTube:**
- "Azure AI Search" by Microsoft — search "Azure Cognitive Search hybrid" on YouTube

---

## 3. Installation — Step by Step

### Step 1 — Install Python 3.12

Download from: https://www.python.org/downloads/release/python-3120/

Or via winget:
```powershell
winget install Python.Python.3.12
# Verify:
python --version
# Should show: Python 3.12.x
```

### Step 2 — Clone the Repository

```powershell
git clone https://github.com/milesbusiness/trading-knowledge-assistant
cd trading-knowledge-assistant
```

### Step 3 — Create Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\activate
# Your prompt should now show (.venv)
pip install -r requirements.txt
```

What `requirements.txt` installs:
```
fastapi==0.115.5            ← Web framework
uvicorn[standard]==0.32.1   ← Web server
pydantic==2.10.3            ← Data validation
pydantic-settings==2.6.1    ← Environment variable settings
langchain==0.3.9            ← AI orchestration
langchain-openai==0.2.11    ← Azure OpenAI connector
langchain-community==0.3.9  ← Azure Search connector
azure-search-documents==11.6.0   ← Azure AI Search SDK
azure-storage-blob==12.21.0      ← Azure Blob Storage SDK
azure-core==1.32.0               ← Azure core utilities
openai==1.57.2                   ← OpenAI base SDK
python-multipart==0.0.20         ← File upload support
```

### Step 4 — Set Up Azure Resources

You need:
1. **Azure OpenAI** with `gpt-4o` and `text-embedding-3-large` deployed
2. **Azure AI Search** (Standard tier — required for vector search)
3. **Azure Blob Storage** account (optional but recommended)

Create these at https://portal.azure.com

### Step 5 — Configure Credentials

Copy the example file:
```powershell
Copy-Item .env.example .env
```

Edit `.env`:
```env
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://YOUR-SEARCH.search.windows.net
AZURE_SEARCH_API_KEY=your-search-key-here
AZURE_SEARCH_INDEX_NAME=trading-knowledge

# Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_STORAGE_CONTAINER=trading-documents

# App settings
SEARCH_TOP_K=5
MAX_CHUNK_SIZE=1000
CHUNK_OVERLAP=100
```

### Step 6 — Run

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Expected output:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080
```

---

## 4. Project File Structure

```
trading-knowledge-assistant/
├── app/
│   ├── main.py                   ← FastAPI app creation, router registration, lifespan
│   ├── api/
│   │   └── routes/
│   │       ├── chat.py           ← POST /api/chat endpoint
│   │       └── documents.py      ← POST/GET/DELETE /api/documents endpoints
│   └── core/
│       ├── config.py             ← Reads .env into a Settings object
│       ├── azure_search.py       ← Creates the Azure AI Search index on startup
│       ├── rag_pipeline.py       ← LangChain chain, session memory, query logic
│       └── document_ingestion.py ← Chunking, embedding, and indexing documents
├── .env.example                  ← Template for .env (shows what variables are needed)
├── Dockerfile                    ← Container build instructions
└── requirements.txt              ← Python package list
```

---

## 5. Code Walkthrough — Every File Explained

### `app/main.py` — Application Entry Point

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_index_exists()
    yield
```
A **lifespan context manager** — runs `ensure_index_exists()` once when the app starts (before any requests). This creates the Azure AI Search index if it doesn't exist yet. The `yield` is where the app runs; code after yield would run on shutdown.

```python
app = FastAPI(
    title="Trading Knowledge Assistant",
    description="LangChain RAG assistant for trading domain knowledge.",
    version="1.0.0",
    lifespan=lifespan,
)
```
Creates the FastAPI application. The `title` and `description` appear at `/docs`.

```python
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
```
CORS (Cross-Origin Resource Sharing) — allows a browser-based frontend to call this API from a different domain.

```python
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
```
Registers both route groups. All chat routes are prefixed with `/api/chat`, all document routes with `/api/documents`.

---

### `app/core/rag_pipeline.py` — The Core AI Logic

This is the most important file. It implements Retrieval-Augmented Generation (RAG).

```python
_sessions: dict[str, ConversationBufferWindowMemory] = {}
```
A module-level dictionary that holds conversation memory for each session. Key = `session_id` (string), Value = a LangChain memory object with the last 10 turns. This is in-memory — sessions are lost on server restart. Production would use Redis.

```python
def get_llm():
    return AzureChatOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        azure_deployment=settings.azure_openai_chat_deployment,
        temperature=0.1,
        max_tokens=2000,
        streaming=True,
    )
```
Creates a connection to Azure OpenAI GPT-4o. `temperature=0.1` is low — we want consistent, factual answers not creative variation. `streaming=True` means tokens arrive progressively (faster perceived response).

```python
def get_vector_store():
    return AzureSearch(
        azure_search_endpoint=settings.azure_search_endpoint,
        azure_search_key=settings.azure_search_api_key,
        index_name=settings.azure_search_index_name,
        embedding_function=get_embeddings().embed_query,
        search_type="hybrid",
        semantic_configuration_name="trading-semantic",
    )
```
Creates a LangChain-compatible wrapper around Azure AI Search. `search_type="hybrid"` is key — this means every query does both:
- BM25 keyword search (exact word matching, great for ticker symbols and regulation references)
- Vector semantic search (meaning-based, great for conceptual questions)

Azure AI Search fuses both results using Reciprocal Rank Fusion.

```python
SYSTEM_PROMPT = """You are a trading domain knowledge assistant...
Use the provided context to answer. Always cite your sources by mentioning the document name.
If the context does not contain the answer, say so clearly — do not hallucinate.

Context:
{context}

Chat History:
{chat_history}

Question: {question}
"""
```
The system prompt has three variable placeholders:
- `{context}` — filled with the retrieved document chunks
- `{chat_history}` — filled with the last N conversation turns
- `{question}` — filled with the current user message

The explicit "do not hallucinate" instruction is critical for a knowledge assistant — without it, the model will invent answers when documents don't contain the answer.

```python
def get_session_memory(session_id: str) -> ConversationBufferWindowMemory:
    if session_id not in _sessions:
        _sessions[session_id] = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10,                 # Keep the last 10 turns
        )
    return _sessions[session_id]
```
Creates a new memory object for each unique `session_id`, or returns the existing one. `k=10` means up to 10 pairs of (human message, AI response) are remembered.

```python
chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vector_store.as_retriever(search_kwargs={"k": settings.search_top_k}),
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt},
    return_source_documents=True,
)
result = await chain.ainvoke({"question": question})
```
The LangChain chain does all the heavy lifting:
1. Takes the question + chat history
2. Reformulates the question (if it's a follow-up) into a standalone query
3. Runs the hybrid search
4. Retrieves top-5 most relevant chunks
5. Builds the prompt (system + history + chunks + question)
6. Calls GPT-4o
7. Stores the result in memory for next turn

`return_source_documents=True` — makes the chain also return which document chunks were used, so we can include citations in the response.

---

### `app/core/document_ingestion.py` — How Documents Are Indexed

```python
def _chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
```
Splits a document into 1,000-character chunks with 100-character overlap. The overlap ensures that if a sentence spans two chunks, both chunks contain part of it — so the retrieval finds the relevant passage even if it's split across a boundary.

```python
for i, chunk in enumerate(chunks):
    vector = embeddings.embed_query(chunk)   # 1536-dimensional float array
    documents.append({
        "id": f"{document_id}-{i}",
        "content": chunk,
        "content_vector": vector,           # stored in Azure AI Search vector field
        "document_name": filename,
        "page_number": i + 1,
        "category": _detect_category(chunk),
    })
search_client.upload_documents(documents)
```
For each chunk: generates a 1536-dimensional embedding vector using `text-embedding-3-large`, then uploads it to Azure AI Search with all metadata.

```python
def _detect_category(text: str) -> str:
    lower = text.lower()
    if "mifid" in lower or "emir" in lower or "regulation" in lower:
        return "regulatory"
    if "strategy" in lower or "alpha" in lower or "signal" in lower:
        return "strategy"
    if "risk" in lower or "var" in lower or "exposure" in lower:
        return "risk"
    return "general"
```
Simple keyword-based category detection. This allows analysts to filter queries to a specific category (e.g., only search regulatory documents).

---

### `app/api/routes/chat.py` — The Chat Endpoint

```python
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"    # If no session_id provided, uses "default"
```

```python
@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    result = await run_rag_query(request.message, request.session_id)
    return ChatResponse(**result)
```
Minimal: validates input, delegates to `run_rag_query`, returns typed response. FastAPI automatically validates the request body against `ChatRequest` and validates the return value against `ChatResponse`.

---

## 6. How to Run and View Output

### Start the Server

```powershell
cd trading-knowledge-assistant
.venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Step 1: Open the API Documentation

Open in browser: **http://localhost:8080/docs**

You will see the Swagger UI with all endpoints: Chat, Documents, Health.

### Step 2: Upload a Document

In the Swagger UI, expand `POST /api/documents`, click "Try it out", select a text or PDF file, and click "Execute".

Or via curl:
```bash
curl -X POST http://localhost:8080/api/documents \
  -F "file=@your-document.txt" \
  -F "category=strategy"
```

Response:
```json
{
  "document_id": "3f7b2c1a-...",
  "filename": "your-document.txt",
  "chunks_indexed": 47
}
```

### Step 3: Ask a Question

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/api/chat" `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"message": "What are the key risk management procedures?", "session_id": "my-session-1"}'
```

Response:
```json
{
  "answer": "According to the Risk Management Framework (Section 3), the key procedures are...",
  "sources": [
    {
      "document_name": "your-document.txt",
      "page_number": 4,
      "excerpt": "Risk management procedures include daily VaR calculation..."
    }
  ],
  "session_id": "my-session-1"
}
```

### Step 4: Follow-Up Question (Multi-Turn)

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/api/chat" `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"message": "What is the VaR limit mentioned there?", "session_id": "my-session-1"}'
```

The system understands "mentioned there" refers to the risk management procedures from the previous turn — because the session memory is active.

### Health Check

```bash
curl http://localhost:8080/health
# {"status":"healthy","service":"trading-knowledge-assistant"}
```

### List Uploaded Documents

```bash
curl http://localhost:8080/api/documents
```

---

## Common Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: No module named 'fastapi'` | Virtual environment not activated | Run `.venv\Scripts\activate` |
| `AZURE_SEARCH_ENDPOINT not set` | `.env` file missing or wrong path | Ensure `.env` is in the project root and all variables are filled |
| `404 Not Found` for Azure Search index | Index creation failed on startup | Check startup logs; the `ensure_index_exists()` call should create it automatically |
| Session memory resets | App was restarted | In-memory sessions don't persist — use same `session_id` within same server run |
| Answers say "No relevant documents found" | No documents uploaded yet | Upload at least one document first via `POST /api/documents` |
