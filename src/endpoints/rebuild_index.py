from fastapi import APIRouter, HTTPException
from src.services.vector_store_service import remove_all_documents, add_document
from src.services.embeding_service import EmbeddingService
from src.utils.logger_config import AppLogger
import logging

logger = AppLogger().logger
router = APIRouter()

embedding_service = EmbeddingService()

@router.post("/rebuild-index/")
async def rebuild_index(documents: list[dict]):
    """
    Rebuild the Pinecone index with new documents.
    This will delete the existing namespace content and re-insert new data.
    """
    try:
        if not documents:
            raise ValueError("No documents provided for rebuilding the index.")

        logger.info("Rebuilding Pinecone index...")

        # Clear all data in current namespace
        remove_all_documents()
        logger.info("Existing namespace cleared.")

        # Process and add each document
        for doc in documents:
            document_id = doc.get("id")
            content = doc.get("content")
            metadata = doc.get("metadata", {})

            if not document_id or not content:
                raise ValueError(f"Document with ID '{document_id}' is missing required fields.")

            add_document(document_id=document_id, text=content, metadata=metadata)
            logger.info(f"Document {document_id} added to the index.")

        logger.info("Index rebuilt successfully.")
        return {"status": "success", "message": "Index rebuilt with provided documents."}

    except Exception as e:
        logger.error(f"Failed to rebuild the index: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
