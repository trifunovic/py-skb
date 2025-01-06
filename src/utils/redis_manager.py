import redis.asyncio as redis
from redis.exceptions import TimeoutError, ConnectionError
import asyncio
from src.config import Config
from src.utils.logger_config import AppLogger

# Initialize logger
app_logger = AppLogger()
logger = app_logger.logger

# Private Redis client (do not access directly)
_redis_client = None

async def initialize_redis(max_retries: int = 5, retry_delay: int = 2):
    """
    Initializes the Redis client and stores the instance.
    """
    global _redis_client
    config = Config()
    logger.info("Initializing Redis...")

    for attempt in range(1, max_retries + 1):
        try:
            _redis_client = redis.Redis(
                host=config.redis_host,
                port=int(config.redis_port),
                password=config.redis_access_key,
                ssl=config.redis_use_ssl,
                decode_responses=True
            )
            logger.debug(f"Attempting to ping Redis (attempt {attempt})...")
            await _redis_client.ping()
            logger.info("Redis initialized successfully.")
            return _redis_client
        except (TimeoutError, ConnectionError) as e:
            logger.warning(f"Redis connection attempt {attempt}/{max_retries} failed: {e}")
            if attempt < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error("Max retries reached. Redis initialization failed.")
                _redis_client = None
                raise Exception("Failed to connect to Redis after multiple attempts.")

async def shutdown_redis():
    """
    Shuts down the Redis connection.
    """
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        logger.info("Redis client connection closed.")
        _redis_client = None

def get_redis_client():
    """
    Returns the Redis client instance.
    """
    if _redis_client is None:
        raise Exception("Redis client has not been initialized.")
    return _redis_client
