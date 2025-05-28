from typing import List
from fastapi import APIRouter, HTTPException
from src.models.request_models import AddDocumentRequest, BulkAddDocumentsRequest
from src.models.response_models import AddDocumentResponse, AddDocumentsResponse
from src.services.vector_store_service import insert_document
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/add-document/", response_model=AddDocumentResponse)
async def add_document(doc: AddDocumentRequest):
    try:
        result = insert_document(doc)
        logger.info(f"Document {doc.id} inserted successfully.")
        return AddDocumentResponse(id=doc.id, status="inserted")
    except Exception as e:
        logger.error(f"Failed to insert document: {str(e)}")
        return AddDocumentResponse(hasErrors=True, error=str(e), id="", status="failed")

@router.post("/add-documents/", response_model=AddDocumentsResponse)
async def add_documents_route(request: BulkAddDocumentsRequest):
    docs = request.documents
    try:
        results = []
        for doc in docs:
            result = insert_document(doc)
            results.append(result)
        logger.info(f"{len(results)} documents inserted.")
        return AddDocumentsResponse(inserted=results)
    except Exception as e:
        logger.error(f"Bulk insert failed: {str(e)}")
        return AddDocumentsResponse(hasErrors=True, error=str(e), inserted=[])
