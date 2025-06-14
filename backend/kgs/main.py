from fastapi import FastAPI, HTTPException
import random
import string
import os
from typing import List
import asyncio
from database.redis_client import (
    add_available_keys,
    get_available_keys,
    add_used_keys,
    remove_used_key,
    is_key_used,
    get_available_keys_count
)

app = FastAPI()

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
        if not is_key_used(key):
            new_keys.add(key)
    
    # Add new keys to available set
    if new_keys:
        add_available_keys(*new_keys)
    return list(new_keys)

async def maintain_key_pool():
    """Background task to maintain minimum number of available keys"""
    while True:
        available_count = get_available_keys_count()
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
    if get_available_keys_count() == 0:
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
    keys = get_available_keys(count)
    
    if not keys:
        # If not enough keys, generate more
        keys = await generate_keys(count)
    
    # Move keys to used set
    if keys:
        add_used_keys(*keys)
    
    return {"codes": keys}

@app.post("/codes/return")
async def return_code(code: str) -> dict:
    """Return a code to the available pool"""
    # Check if code is in used set
    if not is_key_used(code):
        raise HTTPException(status_code=400, detail="Code not found in used set")
    
    # Move code from used to available set
    remove_used_key(code)
    add_available_keys(code)
    
    return {"status": "success"} 