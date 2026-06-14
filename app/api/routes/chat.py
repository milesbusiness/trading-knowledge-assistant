from fastapi import APIRouter
from pydantic import BaseModel
from app.core.rag_pipeline import run_rag_query

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]
    session_id: str


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    result = await run_rag_query(request.message, request.session_id)
    return ChatResponse(**result)
