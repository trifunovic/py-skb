from fastapi import APIRouter, HTTPException
from src.services.vector_store_service import remove_all_documents, add_document
from src.services.embedding_service import EmbeddingService
from src.utils.logger_config import AppLogger
from src.models.request_models import RebuildIndexRequest
import json

router = APIRouter()
logger = AppLogger().logger

@router.post("/rebuild-index/")
async def rebuild_index(request: RebuildIndexRequest):
    try:
        documents = request.documents
        if not documents:
            raise ValueError("No documents provided for rebuilding the index.")

        logger.info("Rebuilding Pinecone index with %d documents...", len(documents))
        remove_all_documents()
        logger.info("Namespace cleared.")

        for doc in documents:
            if not doc.id or not doc.content:
                raise ValueError(f"Invalid document: {doc}")

            # Iskorišćavamo istu funkciju kao za add_document
            add_document(document_id=doc.id, text=doc.content, metadata=doc.metadata or {})

        return {"status": "success", "message": "Index rebuilt", "count": len(documents)}

    except Exception as e:
        logger.error(f"Error rebuilding index: {e}")
        raise HTTPException(status_code=500, detail=str(e))
