from fastapi import APIRouter, HTTPException
from pinecone import Pinecone
from src.config import Config

router = APIRouter()
config = Config()

@router.get("/test-pinecone")
async def test_pinecone():
    """
    Test connectivity to the Pinecone service and list indexes.
    """
    try:
        # Get Pinecone credentials from Config
        api_key = config.pinecone_api_key
        cloud = config.pinecone_cloud
        region = config.pinecone_region

        if not api_key or not cloud or not region:
            raise HTTPException(
                status_code=500,
                detail="Pinecone API key, region, or cloud is not set."
            )

        # Initialize Pinecone client (modern SDK v3+)
        pc = Pinecone(api_key=api_key)

        # List indexes
        indexes = pc.list_indexes().names()
        return {"status": "success", "indexes": indexes}

    except Exception as e:
        return {"status": "error", "details": str(e)}
