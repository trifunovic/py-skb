import os
from fastapi import APIRouter, HTTPException
import redis.asyncio as redis
from config import config

router = APIRouter()

# Initialize Redis client globally
redis_client = None

@router.on_event("startup")
async def initialize_redis():
    """
    Initialize the Redis client during application startup.
    """
    global redis_client
    try:
        redis_client = redis.from_url(f"redis://{config.redis_host}:6379", decode_responses=True)
        # Test Redis connection
        await redis_client.ping()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize Redis: {str(e)}")


@router.get("/test-redis")
async def test_redis():
    """
    Test connectivity to the Redis server.
    """
    try:
        if redis_client is None:
            raise HTTPException(status_code=500, detail="Redis client is not initialized.")
        
        pong = await redis_client.ping()
        return {"status": "success", "response": pong}
    except Exception as e:
        return {"status": "error", "details": str(e)}
