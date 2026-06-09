from pydantic import BaseModel, HttpUrl
from typing import Optional

class URLRequest(BaseModel):
    url: HttpUrl

class URLCheckResponse(BaseModel):
    url: str
    score: int
    is_safe: bool
    risk_level: str
    threat_type: Optional[str] = None
    details: dict