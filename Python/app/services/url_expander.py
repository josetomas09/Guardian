import httpx

SHORTENERS = [
    "bit.ly", "t.co", "tinyurl.com", "goo.gl", "ow.ly",
    "short.link", "buff.ly", "rb.gy", "cutt.ly", "is.gd"
]

def is_shortened(url: str) -> bool:
    return any(shortener in url for shortener in SHORTENERS)

async def expand(url: str) -> str:
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=5) as client:
            response = await client.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
                }
            )
            return str(response.url)
    except Exception:
        return url