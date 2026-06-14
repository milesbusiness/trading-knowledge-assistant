import uuid
import logging
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.storage.blob import BlobServiceClient
from app.core.config import settings
from app.core.rag_pipeline import get_embeddings

logger = logging.getLogger(__name__)


def _get_search_client() -> SearchClient:
    return SearchClient(
        endpoint=settings.azure_search_endpoint,
        index_name=settings.azure_search_index_name,
        credential=AzureKeyCredential(settings.azure_search_api_key)
    )


def _chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


async def ingest_document(filename: str, content: bytes) -> dict:
    document_id = str(uuid.uuid4())

    # Store in blob
    try:
        blob_client = BlobServiceClient.from_connection_string(settings.azure_storage_connection_string)
        container = blob_client.get_container_client(settings.azure_storage_container)
        container.upload_blob(name=f"{document_id}/{filename}", data=content, overwrite=True)
    except Exception as e:
        logger.warning(f"Blob upload failed (non-fatal): {e}")

    # Decode and chunk
    text = content.decode("utf-8", errors="replace")
    chunks = _chunk_text(text, settings.max_chunk_size, settings.chunk_overlap)

    # Embed and index
    embeddings = get_embeddings()
    search_client = _get_search_client()

    documents = []
    for i, chunk in enumerate(chunks):
        try:
            vector = embeddings.embed_query(chunk)
        except Exception:
            vector = [0.0] * 1536

        documents.append({
            "id": f"{document_id}-{i}",
            "document_id": document_id,
            "document_name": filename,
            "content": chunk,
            "page_number": i + 1,
            "category": _detect_category(chunk),
            "content_vector": vector,
        })

    search_client.upload_documents(documents)
    logger.info(f"Indexed {len(documents)} chunks for {filename}")

    return {
        "document_id": document_id,
        "filename": filename,
        "chunks_indexed": len(documents),
    }


async def list_documents() -> list[dict]:
    search_client = _get_search_client()
    results = search_client.search("*", select=["document_id", "document_name"], top=1000)
    seen = {}
    for r in results:
        doc_id = r["document_id"]
        if doc_id not in seen:
            seen[doc_id] = r["document_name"]
    return [{"document_id": k, "filename": v} for k, v in seen.items()]


async def delete_document(document_id: str):
    search_client = _get_search_client()
    results = list(search_client.search("*", filter=f"document_id eq '{document_id}'", select=["id"]))
    if results:
        search_client.delete_documents([{"id": r["id"]} for r in results])
    logger.info(f"Deleted document {document_id}")


def _detect_category(text: str) -> str:
    lower = text.lower()
    if "mifid" in lower or "emir" in lower or "regulation" in lower:
        return "regulatory"
    if "strategy" in lower or "alpha" in lower or "signal" in lower:
        return "strategy"
    if "risk" in lower or "var" in lower or "exposure" in lower:
        return "risk"
    return "general"
