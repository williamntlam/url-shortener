from models.url_schema import UrlRequestObject, UrlResponseObject
from database.models import URLModel
from database.db import get_db
from database.redis_client import cache_url, get_cached_url, delete_cached_url
from database.kgs_client import kgs_client
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

url_storage = {}

# Use a Key Generation Service (KGS) that generates random six letter strings beforehand 
# and stores them in the database.

# When a new URL is created, use one of the randomly generated strings stored in this database.

# Have a table for used keys and unused keys.
# Ensure synchronization and locks.
# Single point of failure at KGS -> Have a replica.
# Implement hashing to make it faster (have app server cache some keys).

# Do hash based partitioning with storage (Consistent Hashing).

# Either use Redis or implement my own caching method.
# Maybe it's good practice to do my own caching and then containerize it 
# To practice Docker and Kubernetes.

async def create_short_url(payload: UrlRequestObject, db: Session) -> UrlResponseObject:
    # Get a short code from KGS
    short_codes = await kgs_client.get_short_codes(count=1)
    if not short_codes:
        raise HTTPException(status_code=503, detail="No short codes available")
    
    short_code = short_codes[0]
    shortened_url = f"http://shorturl/url/{short_code}"
    current_time = datetime.utcnow()

    # Create new URL record
    url_record = URLModel(
        original_url=payload.url,
        short_code=short_code,
        created_at=current_time
    )

    # Save to database
    db.add(url_record)
    db.commit()
    db.refresh(url_record)

    # Prepare response data
    response_data = {
        "url": payload.url,
        "shortened_url": shortened_url,
        "short_code": short_code,
        "created_at": current_time,
        "is_expired": False,
        "is_one_time": False,
        "is_active": True
    }

    # Cache in Redis
    cache_url(short_code, response_data)

    return UrlResponseObject(**response_data)

async def delete_url(short_code: str, db: Session) -> bool:
    # Check cache first
    cached_url = get_cached_url(short_code)
    if cached_url:
        delete_cached_url(short_code)

    # Delete from database
    url_record = db.query(URLModel).filter(URLModel.short_code == short_code).first()
    if url_record:
        db.delete(url_record)
        db.commit()
        # Return the short code to KGS
        await kgs_client.return_short_code(short_code)
        return True
    return False

async def get_original_url(short_code: str, db: Session) -> UrlRequestObject:
    # Try to get from cache first
    cached_url = get_cached_url(short_code)
    if cached_url:
        return UrlRequestObject(**cached_url)

    # If not in cache, get from database
    url_record = db.query(URLModel).filter(URLModel.short_code == short_code).first()
    if not url_record:
        raise HTTPException(status_code=404, detail="URL not found")

    # Check if URL is expired or inactive
    if url_record.is_expired or not url_record.is_active:
        raise HTTPException(status_code=410, detail="URL is no longer available")

    # Increment click count
    url_record.clicks += 1
    db.commit()

    # Prepare response data
    response_data = {
        "url": url_record.original_url,
        "shortened_url": f"http://shorturl/url/{url_record.short_code}",
        "short_code": url_record.short_code,
        "created_at": url_record.created_at,
        "is_expired": url_record.is_expired,
        "is_one_time": url_record.is_one_time,
        "is_active": url_record.is_active
    }

    # Cache the result
    cache_url(short_code, response_data)

    return UrlRequestObject(**response_data)

async def get_analytics(short_code: str) -> UrlRequestObject:
    # I believe redis is also used for analytics.
    # Have two redis pods maybe?
    pass