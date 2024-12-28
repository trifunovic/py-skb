from fastapi import APIRouter, HTTPException
from app.services.embeding_service import EmbeddingService  # Relative import
from app.utils.pinecone_utils import get_pinecone_index
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize the embedding service
embedding_service = EmbeddingService()

@router.post("/rebuild-index/")
async def rebuild_index(documents: list[dict]):
    """
    Rebuild the Pinecone index with new documents.
    This will delete the existing index and recreate it with the new data.
    """
    try:
        if not documents:
            raise ValueError("No documents provided for rebuilding the index.")

        logger.info("Rebuilding Pinecone index...")

        # Get or recreate the index
        index = get_pinecone_index()
        index.delete(delete_all=True)  # Clear existing data
        logger.info("Existing index cleared.")

        # Process and add each document
        for doc in documents:
            document_id = doc.get("id")
            content = doc.get("content")
            metadata = doc.get("metadata", {})

            if not document_id or not content:
                raise ValueError(f"Document with ID '{document_id}' is missing required fields.")

            # Generate embedding using the centralized embedding service
            embedding = embedding_service.generate_embedding(content).tolist()

            # Upsert into the index
            index.upsert([(document_id, embedding, metadata)])
            logger.info(f"Document {document_id} added to the index.")

        logger.info("Index rebuilt successfully.")
        return {"status": "success", "message": "Index rebuilt with provided documents."}

    except Exception as e:
        logger.error(f"Failed to rebuild the index: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
