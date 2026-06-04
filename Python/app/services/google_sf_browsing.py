import httpx
import hashlib
import base64
import os
from app.services import safebrowsing_pb2

API_KEY = os.getenv("GOOGLE_API_KEY")
API_URL = "https://safebrowsing.googleapis.com/v5/hashes:search"

def _get_hash_prefix(url: str) -> str:
    digest = hashlib.sha256(url.encode()).digest()
    return base64.b64encode(digest[:4]).decode()

async def check(url: str) -> dict:
    try:
        hash_prefix = _get_hash_prefix(url)

        async with httpx.AsyncClient() as client:
            response = await client.get(
                API_URL,
                params={
                    "key": API_KEY,
                    "hashPrefixes": hash_prefix
                }
            )

        proto_response = safebrowsing_pb2.SearchHashesResponse()
        proto_response.ParseFromString(response.content)

        threats = list(proto_response.full_hashes)

        return {
            "is_safe": len(threats) == 0,
            "threats": [str(t) for t in threats]
        }

    except httpx.RequestError:
        return {
            "is_safe": None,
            "threats": [],
            "error": "No se pudo conectar con Google Safe Browsing"
        }
    except Exception as e:
        return {
            "is_safe": None,
            "threats": [],
            "error": str(e)
        }