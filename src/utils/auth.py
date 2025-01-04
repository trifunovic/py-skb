from fastapi import HTTPException, Request
import os
import logging

logger = logging.getLogger("auth")
logger.setLevel(logging.DEBUG)

async def authenticate(request: Request):
    api_key = request.headers.get("Authorization")
    expected_key = os.getenv("KNOWLEDGE_API_KEY")
    logger.debug(f"Received API Key: {api_key}, Expected Key: {expected_key}")

    if api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")
