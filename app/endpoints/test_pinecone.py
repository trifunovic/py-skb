from fastapi import APIRouter, HTTPException
from pinecone import Pinecone
from config import config

router = APIRouter()

@router.get("/test-pinecone")
async def test_pinecone():
    """
    Test connectivity to the Pinecone service and list indexes.
    """
    try:
        # Get Pinecone API key and environment from Config
        api_key = config.pinecone_api_key
        environment = config.pinecone_environment
        if not api_key or not environment:
            raise HTTPException(
                status_code=500,
                detail="Pinecone API key or environment is not set."
            )
        
        # Initialize Pinecone client
        pc = Pinecone(api_key=api_key, environment=environment)

        # List indexes
        indexes = pc.list_indexes().names()
        return {"status": "success", "indexes": indexes}
    
    except Exception as e:
        # Return detailed error for debugging
        return {"status": "error", "details": str(e)}
