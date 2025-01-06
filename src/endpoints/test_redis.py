from fastapi import APIRouter, HTTPException
from src.utils.redis_manager import get_redis_client
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/test-redis")
async def test_redis_connection():
    """
    Endpoint to test Redis connection.
    """
    redis_client = get_redis_client()  # Get Redis client instance
    try:
        await redis_client.ping()
        logger.info("Redis ping successful.")
        return {"status": "connected", "message": "Redis ping successful!"}
    except Exception as e:
        logger.error(f"Redis ping failed: {e}")
        raise HTTPException(status_code=500, detail=f"Redis ping failed: {str(e)}")
