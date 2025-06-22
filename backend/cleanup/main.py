import os
import logging
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import DictCursor
import redis
from typing import List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class URLCleanupService:
    def __init__(self):
        self.db_conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        self.redis_client = redis.from_url(os.getenv('REDIS_URL'))
        
    def get_expired_urls(self) -> List[Tuple[str, str]]:
        """Get all expired URLs from the database."""
        with self.db_conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT short_url, original_url 
                FROM urls 
                WHERE expires_at < NOW()
            """)
            return cur.fetchall()

    def delete_from_database(self, short_url: str) -> None:
        """Delete an expired URL from the database."""
        with self.db_conn.cursor() as cur:
            cur.execute("DELETE FROM urls WHERE short_url = %s", (short_url,))
        self.db_conn.commit()

    def delete_from_redis(self, short_url: str) -> None:
        """Delete an expired URL from Redis cache."""
        self.redis_client.delete(f"url:{short_url}")

    def cleanup_expired_urls(self) -> None:
        """Main cleanup function that removes expired URLs from both database and cache."""
        try:
            expired_urls = self.get_expired_urls()
            logger.info(f"Found {len(expired_urls)} expired URLs to clean up")

            for url in expired_urls:
                short_url = url['short_url']
                try:
                    # Delete from database first
                    self.delete_from_database(short_url)
                    # Then delete from cache
                    self.delete_from_redis(short_url)
                    logger.info(f"Successfully cleaned up expired URL: {short_url}")
                except Exception as e:
                    logger.error(f"Error cleaning up URL {short_url}: {str(e)}")
                    continue

            logger.info("Cleanup completed successfully")
        except Exception as e:
            logger.error(f"Error during cleanup process: {str(e)}")
            raise
        finally:
            self.db_conn.close()
            self.redis_client.close()

def main():
    """Main entry point for the cleanup service."""
    try:
        service = URLCleanupService()
        service.cleanup_expired_urls()
    except Exception as e:
        logger.error(f"Fatal error in cleanup service: {str(e)}")
        raise

if __name__ == "__main__":
    main() 