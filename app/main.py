from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from app.config import Config
from app.endpoints.add_document import router as add_document_router
from app.endpoints.search import router as search_router
from app.endpoints.rebuild_index import router as rebuild_index_router
from app.endpoints.test_pinecone import router as test_pinecone_router
from app.endpoints.test_redis import router as test_redis_router
from app.endpoints.test_openai import router as test_openai_router
from app.endpoints.test_config import router as test_config_router
from dotenv import load_dotenv
import os

# Load environment variables from .env.local if available
dotenv_path = os.path.join(os.path.dirname(__file__), ".env.local")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=False)  # Prevent overriding system variables
    print(f"Loaded environment variables from {dotenv_path}")
else:
    print(f"Warning: {dotenv_path} not found. Using system environment variables.")

# Load configuration
config = Config()

# Create the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins,  # Use allowed origins from Config
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize Redis client globally
redis_client = None

@app.on_event("startup")
async def startup():
    """
    Initialize Redis for rate limiting and other startup tasks.
    """
    global redis_client
    redis_url = f"redis://{config.redis_host}:6379"
    redis_client = redis.from_url(redis_url, decode_responses=True)
    try:
        await redis_client.ping()  # Test Redis connection
        print(f"Connected to Redis at {redis_url}")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        raise RuntimeError("Redis connection failed. Check your Redis configuration.")

    try:
        await FastAPILimiter.init(redis_client)  # Initialize FastAPI rate limiting
        print("FastAPI Limiter initialized.")
    except Exception as e:
        print(f"Failed to initialize FastAPI Limiter: {e}")
        raise RuntimeError("Rate limiting setup failed.")

# Register routers
app.include_router(add_document_router)
app.include_router(search_router)
app.include_router(rebuild_index_router)
app.include_router(test_pinecone_router)  # Separate test-pinecone endpoint
app.include_router(test_redis_router)  # Separate test-redis endpoint
app.include_router(test_openai_router)  # Separate test-openai endpoint
app.include_router(test_config_router)  # Separate test-config endpoint

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Pinecone-Powered Knowledge Base!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.on_event("shutdown")
async def shutdown():
    """
    Cleanup tasks when the application shuts down.
    """
    global redis_client
    if redis_client:
        await redis_client.close()
        print("Redis client connection closed.")
