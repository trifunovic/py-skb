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
)
from src.endpoints.chat import router as chat_router
from src.endpoints.ask import router as ask_router
from src.utils.logger_config import AppLogger
from src.utils.redis_manager import initialize_redis, shutdown_redis, get_redis_client
from src.services.vector_store_service import ensure_index_exists
from src.utils.print_config import print_config
from src.services.embedding_service import embedding_service

app = FastAPI()
config = Config()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_logger = AppLogger()
logger = app_logger.logger

@app.on_event("startup")
async def startup():
    logger.info("************ Starting FastAPI application... ************")
    app_logger.log_system_info()
    print_config(config, embedding_service)
    ensure_index_exists()

    await initialize_redis()
    redis_client = get_redis_client()

    await FastAPILimiter.init(redis_client)
    logger.info("FastAPILimiter initialized successfully.")
    logger.info("************ Startup tasks completed. ************")

@app.on_event("shutdown")
async def shutdown():
    await shutdown_redis()
    logger.info("FastAPI application shutting down.")

# Register routers
app.include_router(add_document_router)
app.include_router(search_router)
app.include_router(ask_router)
app.include_router(chat_router)

app.include_router(rebuild_index_router)
app.include_router(list_documents_router)

app.include_router(test_pinecone_router)
app.include_router(test_redis_router)
app.include_router(test_openai_router)
app.include_router(test_config_router)

@app.get("/health/redis")
async def redis_health_check():
    redis_client = get_redis_client()
    try:
        await redis_client.ping()
        return {"status": "Redis is healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Pinecone-Powered Knowledge Base!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.app_port)
