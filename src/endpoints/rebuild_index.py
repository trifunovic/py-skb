from fastapi import APIRouter, HTTPException, status
from src.services.vector_store_service import remove_all_documents, add_document
from src.services.embeding_service import EmbeddingService
from src.utils.logger_config import AppLogger
from src.models.request_models import RebuildIndexRequest
from src.models.response_models import RebuildIndexResponse

logger = AppLogger().logger
router = APIRouter()
embedding_service = EmbeddingService()

@router.post("/rebuild-index/", status_code=status.HTTP_200_OK, response_model=RebuildIndexResponse)
async def rebuild_index(request: RebuildIndexRequest):
    """
    Rebuild the Pinecone index with new documents.
    This will delete the existing namespace content and re-insert new data.
    """
    try:
        documents = request.documents
        if not documents:
            return RebuildIndexResponse(
                hasErrors=True,
                error="No documents provided for rebuilding the index.",
                message=""
            )

        logger.info("Rebuilding Pinecone index...")

        remove_all_documents()
        logger.info("Existing namespace cleared.")

        for doc in documents:
            add_document(document_id=doc.id, text=doc.content, metadata=doc.metadata)
            logger.info(f"✅ Document added: {doc.id}")

        logger.info("Index rebuilt successfully with %d documents.", len(documents))
        return RebuildIndexResponse(
            message=f"Index rebuilt with {len(documents)} documents."
        )

    except Exception as e:
        logger.error("❌ Failed to rebuild index: %s", str(e))
        return RebuildIndexResponse(
            hasErrors=True,
            error=f"Failed to rebuild index: {str(e)}",
            message=""
        )
