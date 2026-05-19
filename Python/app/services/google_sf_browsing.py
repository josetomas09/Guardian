import httpx
import os

API_KEY = os.getenv("GOOGLE_API_KEY")
API_URL = "https://safebrowsing.googleapis.com/v5/hashes:search"

async def check(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            API_URL,
            params={"key": API_KEY},
            json={ #TODO: add threatTypes
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
                "hashPrefixes": [_get_hash_prefix(url)]
            }
        )
    data = response.json()
    threats = data.get("fullHashes", [])

    return {
        "is_safe": len(threats) == 0,
        "threats": threats
    }

def _get_hash_prefix(url: str) -> str:
    import hashlib, base64
    digest = hashlib.sha256(url.encode()).digest()
    return base64.b64encode(digest[:4]).decode()