import redis
import os
import json

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

# URL caching functions
def cache_url(short_code: str, url_data: dict, expire_time: int = 3600):
    """Cache URL data in Redis"""
    redis_client.setex(
        f"url:{short_code}",
        expire_time,
        json.dumps(url_data)
    )

def get_cached_url(short_code: str) -> dict:
    """Get URL data from Redis cache"""
    data = redis_client.get(f"url:{short_code}")
    return json.loads(data) if data else None

def delete_cached_url(short_code: str):
    """Delete URL data from Redis cache"""
    redis_client.delete(f"url:{short_code}")

# KGS functions
def add_available_keys(*keys: str):
    """Add keys to available keys set"""
    redis_client.sadd("available_keys", *keys)

def get_available_keys(count: int = 1) -> list:
    """Get and remove keys from available set"""
    return redis_client.spop("available_keys", count)

def add_used_keys(*keys: str):
    """Add keys to used keys set"""
    redis_client.sadd("used_keys", *keys)

def remove_used_key(key: str):
    """Remove key from used set"""
    redis_client.srem("used_keys", key)

def is_key_used(key: str) -> bool:
    """Check if key is in used set"""
    return redis_client.sismember("used_keys", key)

def get_available_keys_count() -> int:
    """Get count of available keys"""
    return redis_client.scard("available_keys") 