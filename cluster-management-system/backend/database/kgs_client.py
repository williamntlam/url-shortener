import aiohttp
import os
from typing import List, Optional

KGS_HOST = os.getenv("KGS_HOST", "kgs")
KGS_PORT = os.getenv("KGS_PORT", "3001")
KGS_URL = f"http://{KGS_HOST}:{KGS_PORT}"

class KGSClient:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_short_codes(self, count: int = 1) -> List[str]:
        """Request short codes from the KGS service"""
        if not self.session:
            self.session = aiohttp.ClientSession()

        async with self.session.get(f"{KGS_URL}/codes", params={"count": count}) as response:
            if response.status != 200:
                raise Exception(f"Failed to get short codes: {response.status}")
            data = await response.json()
            return data["codes"]

    async def return_short_code(self, code: str) -> bool:
        """Return an unused short code to the KGS service"""
        if not self.session:
            self.session = aiohttp.ClientSession()

        async with self.session.post(f"{KGS_URL}/codes/return", json={"code": code}) as response:
            return response.status == 200

# Create a singleton instance
kgs_client = KGSClient() 