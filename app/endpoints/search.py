from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi_limiter.depends import RateLimiter
from config import Config
from services.embeding_service import EmbeddingService
from utils.pinecone_utils import get_pinecone_index
import logging
import traceback

embeding_service = EmbeddingService()
logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/search/", dependencies=[Depends(RateLimiter(times=10, seconds=60))], response_class=JSONResponse)
async def search(query: str, request: Request):
    try:
        logger.info(f"Received search query: {query}")

        if not query.strip():
            raise ValueError("Query cannot be empty or whitespace.")

        query_embedding = embeding_service.generate_embedding(query).tolist()

        index = get_pinecone_index()
        results = index.query(vector=query_embedding, top_k=5, include_metadata=True)

        if "matches" not in results or not results["matches"]:
            return {"query": query, "results": [], "warning": "No matching documents found."}

        readable_results = [
            {
                "document_id": match["id"],
                "relevance_score": round(match.get("score", 0), 2),
                "short_answer": embeding_service.refine_answer_based_on_query(
                    query,
                    embeding_service.extract_semantically_relevant_answer(match["metadata"].get("content", ""), query)
                ),
                "details": match["metadata"]
            }
            for match in results["matches"]
        ]

        logger.info(f"Search results: {readable_results}")
        return {"query": query, "results": readable_results}
    except Exception as e:
        logger.error(f"Unhandled exception: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
