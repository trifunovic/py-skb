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
        api_key = config.pinecone_api_key
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="Pinecone API key is not set."
            )

        # Pinecone Management API (v3+)
        pc = Pinecone(api_key=api_key)
        indexes = pc.list_indexes()  # list of dicts

        return {
            "status": "success",
            "indexes": [idx["name"] for idx in indexes],
            "index_details": indexes,
            "project_name": pc.project_name,
            "environment": pc.environment
        }

    except Exception as e:
        return {
            "status": "error",
            "details": str(e)
        }
