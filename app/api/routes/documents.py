from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.document_ingestion import ingest_document, list_documents, delete_document

router = APIRouter()


@router.post("")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(400, "No file provided")
    content = await file.read()
    result = await ingest_document(file.filename, content)
    return result


@router.get("")
async def list_docs():
    return await list_documents()


@router.delete("/{document_id}")
async def delete_doc(document_id: str):
    await delete_document(document_id)
    return {"deleted": document_id}
