import httpx
import base64
import os

API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
API_URL = "https://www.virustotal.com/api/v3/urls"

def _detect_threat_type(categories: dict, results: dict, url: str = "") -> str:
    all_text = " ".join(
        list(categories.values()) +
        [r.get("result", "") for r in results.values() if r.get("result")]
    ).lower()

    # Primero chequeamos la URL como contexto fuerte
    url_lower = url.lower()
    if "unwanted" in url_lower:
        return "unwanted_software"
    if "malware" in url_lower:
        return "malware"
    if "social_engineering" in url_lower or "phishing" in url_lower:
        return "phishing"

    # Luego analizamos categorías
    if any(w in all_text for w in ["phishing", "social engineering", "fraud"]):
        return "phishing"
    if any(w in all_text for w in ["malware", "trojan", "virus", "ransomware"]):
        return "malware"
    if any(w in all_text for w in ["unwanted", "adware", "pup"]):
        return "unwanted_software"
    if any(w in all_text for w in ["suspicious", "spam"]):
        return "suspicious"
    return "malicious"

async def check(url: str) -> dict:
    try:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_URL}/{url_id}",
                headers={"x-apikey": API_KEY}
            )

        if response.status_code == 404:
            return {
                "is_safe": None,
                "malicious_engines": 0,
                "suspicious_engines": 0,
                "total_engines": 0,
                "threat_type": "unknown",
                "categories": {}
            }

        data = response.json()
        attrs = data["data"]["attributes"]
        stats = attrs.get("last_analysis_stats", {})
        categories = attrs.get("categories", {})
        results = attrs.get("last_analysis_results", {})

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        total = sum(stats.values())

        threat_type = None
        if malicious > 0 or suspicious > 0:
            threat_type = _detect_threat_type(categories, results, url)

        return {
            "is_safe": malicious == 0 and suspicious == 0,
            "malicious_engines": malicious,
            "suspicious_engines": suspicious,
            "total_engines": total,
            "threat_type": threat_type,
            "categories": categories
        }

    except httpx.RequestError:
        return {
            "is_safe": None,
            "malicious_engines": 0,
            "suspicious_engines": 0,
            "total_engines": 0,
            "threat_type": None,
            "error": "No se pudo conectar con VirusTotal"
        }
    except Exception as e:
        return {
            "is_safe": None,
            "malicious_engines": 0,
            "suspicious_engines": 0,
            "total_engines": 0,
            "threat_type": None,
            "error": str(e)
        }