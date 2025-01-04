from fastapi import APIRouter, HTTPException, Request
from src.services.embeding_service import EmbeddingService
from src.utils.pinecone_utils import get_pinecone_index
import logging

embeding_service = EmbeddingService()
logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/add-document/")
async def add_document(request: Request):
    try:
        payload = await request.json()
        document_id = payload.get("id")
        content = payload.get("content")
        metadata = payload.get("metadata", {})

        if not document_id or not content:
            raise ValueError("Both 'id' and 'content' fields are required.")

        embedding = embeding_service.generate_embedding(content).tolist()

        index = get_pinecone_index()
        index.upsert([(document_id, embedding, metadata)])

        logger.info(f"Document {document_id} added successfully.")
        return {"status": "success", "document_id": document_id}
    except Exception as e:
        logger.error(f"Failed to add document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
