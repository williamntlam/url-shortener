from models.url_schema import UrlRequestObject, UrlResponseObject
from datetime import datetime
import uuid

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

async def create_short_url(payload: UrlResponseObject) -> UrlRequestObject:
    short_code = str(uuid.uuid())[:8]
    shortened_url = f"http://shorturl/url/{short_code}"

    current_time = datetime.utcnow()

    data = UrlResponseObject(
        url=payload.url,
        shortened_url=shortened_url,
        short_code=short_code,
        created_at=current_time
    )

    url_store[short_code] = data

    return data

async def delete_url(short_code: str) -> UrlRequestObject:
    if short_code in url_store:
        del url_store[short_code]
        return True
    return False

async def get_original_url(short_code: str) -> UrlRequestObject:
    # Access database with short_code as key 
    # and determine if it exists.
    pass
 
async def get_analytics(short_code: str) -> UrlRequestObject:
    # I believe redis is also used for analytics.
    # Have two redis pods maybe?
    pass