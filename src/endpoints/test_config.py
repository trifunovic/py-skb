from fastapi import APIRouter
from src.config import Config
import os
import pinecone

router = APIRouter()
config = Config()

@router.get("/test-config")
async def test_config():
    """
    Test endpoint to display current application configuration variables.
    """
    return {
        "pinecone_index_name": config.pinecone_index_name,
        "pinecone_region": config.pinecone_region,
        "pinecone_cloud": config.pinecone_cloud,
        "pinecone_metric": config.pinecone_metric,
        "pinecone_namespace": config.pinecone_namespace,
        "pinecone_client_version": pinecone.__version__,
        "redis_host": config.redis_host,
        "allowed_origins": config.allowed_origins,
        "openai_model": config.openai_model,
        "model_name": config.model_name,
        "model_type": config.model_type,
        "debug_mode": os.getenv("DEBUG", "False"),
        "log_level": os.getenv("LOG_LEVEL", "info"),
        "pinecone_api_key_present": bool(config.pinecone_api_key),
        "openai_api_key_present": bool(config.openai_api_key),
        "knowledge_api_key_present": bool(config.knowledge_api_key),
        "backend_versiont": (config.backend_version),
    }
