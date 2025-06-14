from fastapi import FastAPI, HTTPException
import redis
import random
import string
import os
from typing import List
import asyncio

app = FastAPI()

# Redis connection
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

# Constants
KEY_LENGTH = 6
MIN_AVAILABLE_KEYS = 1000  # Minimum number of keys to maintain
BATCH_SIZE = 100  # Number of keys to generate in one batch

def generate_random_key() -> str:
    """Generate a random 6-letter string"""
    return ''.join(random.choices(string.ascii_letters, k=KEY_LENGTH))

async def generate_keys(count: int) -> List[str]:
    """Generate unique keys and add them to available keys set"""
    new_keys = set()
    while len(new_keys) < count:
        key = generate_random_key()
        # Check if key exists in either available or used sets
        if not redis_client.sismember("available_keys", key) and not redis_client.sismember("used_keys", key):
            new_keys.add(key)
    
    # Add new keys to available set
    if new_keys:
        redis_client.sadd("available_keys", *new_keys)
    return list(new_keys)

async def maintain_key_pool():
    """Background task to maintain minimum number of available keys"""
    while True:
        available_count = redis_client.scard("available_keys")
        if available_count < MIN_AVAILABLE_KEYS:
            needed = MIN_AVAILABLE_KEYS - available_count
            await generate_keys(min(needed, BATCH_SIZE))
        await asyncio.sleep(60)  # Check every minute

@app.on_event("startup")
async def startup_event():
    """Initialize key pool on startup"""
    # Start background task to maintain key pool
    asyncio.create_task(maintain_key_pool())
    
    # Generate initial keys if none exist
    if redis_client.scard("available_keys") == 0:
        await generate_keys(MIN_AVAILABLE_KEYS)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/codes")
async def get_codes(count: int = 1) -> dict:
    """Get available short codes"""
    if count <= 0:
        raise HTTPException(status_code=400, detail="Count must be positive")
    
    # Get keys from available set
    keys = redis_client.spop("available_keys", count)
    
    if not keys:
        # If not enough keys, generate more
        keys = await generate_keys(count)
    
    # Move keys to used set
    if keys:
        redis_client.sadd("used_keys", *keys)
    
    return {"codes": keys}

@app.post("/codes/return")
async def return_code(code: str) -> dict:
    """Return a code to the available pool"""
    # Check if code is in used set
    if not redis_client.sismember("used_keys", code):
        raise HTTPException(status_code=400, detail="Code not found in used set")
    
    # Move code from used to available set
    redis_client.srem("used_keys", code)
    redis_client.sadd("available_keys", code)
    
    return {"status": "success"} 