from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.api.routes import chat, documents
from app.core.config import settings
from app.core.azure_search import ensure_index_exists


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_index_exists()
    yield


app = FastAPI(
    title="Trading Knowledge Assistant",
    description="LangChain RAG assistant for trading domain knowledge. Hybrid Azure AI Search + GPT-4o.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "trading-knowledge-assistant"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
