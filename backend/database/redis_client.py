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