from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi_limiter.depends import RateLimiter
from src.services.vector_store_service import search_similar, get_all_documents
from src.services.embeding_service import EmbeddingService
from src.utils.logger_config import AppLogger
from src.config import Config
from src.models.request_models import SearchRequest, IdsRequest
from src.models.response_models import SearchResponse, SearchResult, GetAllDocumentsResponse
from typing import List
import traceback

config = Config()
app_logger = AppLogger()
logger = app_logger.logger

embedding_service = EmbeddingService()
router = APIRouter()

@router.post(
    "/search/",
    dependencies=[Depends(RateLimiter(times=config.search_rate_limit, seconds=60))],
    response_model=SearchResponse,
    response_class=JSONResponse
)
async def search(request: SearchRequest, raw_request: Request):
    try:
        client_ip = raw_request.client.host
        logger.info(f"Received search query from {client_ip}: {request.query}")

        if not request.query.strip():
            return SearchResponse(hasErrors=True, error="Query cannot be empty.", query=request.query, results=[])

        results = search_similar(request.query, top_k=request.top_k or config.search_top_k)

        if not results.get("matches"):
            return SearchResponse(query=request.query, results=[], error="No matching documents found.", hasErrors=False)

        readable_results = []
        for match in results["matches"]:
            metadata = getattr(match, "metadata", {}) or {}
            content = metadata.get("content", "")
            short_answer = embedding_service.refine_answer_based_on_query(
                request.query,
                embedding_service.extract_semantically_relevant_answer(content, request.query)
            )

            readable_results.append(SearchResult(
                document_id=getattr(match, "id", "unknown"),
                relevance_score=round(getattr(match, "score", 0), 2),
                short_answer=short_answer,
                details=metadata
            ))

        logger.info(f"Search results: {len(readable_results)} documents found.")
        return SearchResponse(query=request.query, results=readable_results)

    except Exception as e:
        logger.error(f"Unhandled exception: {traceback.format_exc() if config.debug_mode else str(e)}")
        return SearchResponse(query=request.query, results=[], hasErrors=True, error="An unexpected error occurred.")

@router.post("/get-all-documents/", response_model=GetAllDocumentsResponse)
async def get_all_documents_route(req: IdsRequest):
    try:
        documents = get_all_documents(req.ids)
        return GetAllDocumentsResponse(documents=documents)
    except Exception as e:
        return GetAllDocumentsResponse(documents=[], hasErrors=True, error=str(e))
