# app/services/virustotal.py
import httpx
import base64
import os

API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
API_URL = "https://www.virustotal.com/api/v3/urls"


async def check(url: str) -> dict:
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/{url_id}",
            headers={"x-apikey": API_KEY}
        )

    if response.status_code == 404:
        return {"is_safe": True, "message": "URL not in database"}

    stats = response.json()["data"]["attributes"]["last_analysis_stats"]
    malicious = stats.get("malicious", 0)

    return {
        "is_safe": malicious == 0,
        "malicious_engines": malicious,
        "total_engines": sum(stats.values())
    }