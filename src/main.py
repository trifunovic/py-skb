from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from src.config import Config
from src.endpoints import (
    add_document_router,
    search_router,
    rebuild_index_router,
    test_pinecone_router,
    test_redis_router,
    test_openai_router,
    test_config_router,
    list_documents_router,
    langchain_router
)
from src.utils.logger_config import AppLogger
from src.utils.redis_manager import initialize_redis, shutdown_redis, get_redis_client
from src.services.vector_store_service import ensure_index_exists

app = FastAPI()
config = Config()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logger
app_logger = AppLogger()
logger = app_logger.logger

@app.on_event("startup")
async def startup():
    """
    Startup event for initializing Redis and logging.
    """
    logger.info("************ Starting FastAPI application... ************")
    app_logger.log_system_info()
    config.print_config()
    ensure_index_exists()

    await initialize_redis()
    redis_client = get_redis_client()

    await FastAPILimiter.init(redis_client)
    logger.info("FastAPILimiter initialized successfully.")
    logger.info("************ Startup tasks completed. ************")

@app.on_event("shutdown")
async def shutdown():
    """
    Shutdown event to close Redis connection.
    """
    await shutdown_redis()
    logger.info("FastAPI application shutting down.")

# Register routers
app.include_router(add_document_router)
app.include_router(search_router)
app.include_router(rebuild_index_router)
app.include_router(test_pinecone_router)
app.include_router(test_redis_router)
app.include_router(test_openai_router)
app.include_router(test_config_router)
app.include_router(list_documents_router)
app.include_router(langchain_router)

@app.get("/health/redis")
async def redis_health_check():
    """
    Health check endpoint for Redis connection.
    """
    redis_client = get_redis_client()
    try:
        await redis_client.ping()
        return {"status": "Redis is healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

@app.get("/")
async def read_root():
    """
    Root endpoint.
    """
    print("Root endpoint accessed.")
    return {"message": "Welcome to the Pinecone-Powered Knowledge Base!"}

@app.get("/health")
async def health_check():
    """
    Health check for the app.
    """
    print("Health check endpoint accessed.")
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.app_port)
