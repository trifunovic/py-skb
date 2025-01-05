from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from redis.exceptions import TimeoutError, ConnectionError
from src.config import Config
from src.endpoints.add_document import router as add_document_router
from src.endpoints.search import router as search_router
from src.endpoints.rebuild_index import router as rebuild_index_router
from src.endpoints.test_pinecone import router as test_pinecone_router
from src.endpoints.test_redis import router as test_redis_router
from src.endpoints.test_openai import router as test_openai_router
from src.endpoints.test_config import router as test_config_router
from dotenv import load_dotenv
import os
import platform
import psutil
import asyncio

# Load environment variables from .env.local if available
dotenv_path = os.path.join(os.path.dirname(__file__), ".env.prod")
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


# System info function
def print_system_info():
    """
    Prints system information such as OS, memory, and CPU usage.
    """
    print("\n=== System Information ===")
    print(f"OS: {platform.system()} {platform.release()} ({platform.version()})")
    print(f"Architecture: {platform.architecture()[0]}")
    print(f"Processor: {platform.processor()}")
    print(f"CPU Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical")
    print(f"Memory: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB total")
    print(f"Free Memory: {round(psutil.virtual_memory().available / (1024 ** 3), 2)} GB")
    print(f"Disk Usage: {psutil.disk_usage('/').percent}% used of {round(psutil.disk_usage('/').total / (1024 ** 3), 2)} GB")
    print(f"Network Interfaces: {psutil.net_if_addrs()}\n")
    print("==========================")


async def create_redis_client_with_retry(retries: int = 5, delay: int = 2):
    """
    Creates a Redis client with retry logic.
    """
    for attempt in range(retries):
        try:
            redis_url = f"redis://{config.redis_host}:{config.redis_port}"  # Ensure port matches config
            client = redis.Redis(
                host=config.redis_host,
                port=int(config.redis_port),
                password=config.redis_access_key,
                db=0,
                decode_responses=True,
                socket_connect_timeout=5,  # Connection timeout in seconds
                retry_on_timeout=True,
                ssl=True  # Enable SSL/TLS for secure Redis communication
            )
            await client.ping()  # Test connection
            print(f"Connected to Redis on attempt {attempt + 1}")
            return client
        except (TimeoutError, ConnectionError) as e:
            print(f"Redis connection attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
            await asyncio.sleep(delay)
    raise RuntimeError("Failed to connect to Redis after multiple retries. Check your Redis configuration.")


@app.on_event("startup")
async def startup():
    """
    Initialize Redis for rate limiting and other startup tasks.
    """
    print("\nStarting FastAPI application...")
    
    # Print system information and config values
    # print_system_info()
    config.print_config()

    global redis_client
    try:
        redis_client = await create_redis_client_with_retry()
        await FastAPILimiter.init(redis_client)  # Initialize FastAPI rate limiting
        print("FastAPI Limiter initialized successfully.")
    except Exception as e:
        print(f"Redis initialization failed: {e}")
        raise RuntimeError("Redis initialization failed.")


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
    """
    Root endpoint to check if the application is running.
    """
    print("Root endpoint accessed.")
    return {"message": "Welcome to the Pinecone-Powered Knowledge Base!"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint to ensure the app is running.
    """
    print("Health check endpoint accessed.")
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
    print("FastAPI application shutting down.")
