from pydantic import BaseModel, HttpUrl

class URLRequest(BaseModel):
    url: HttpUrl

class URLCheckResponse(BaseModel):
    url: str
    score: int
    is_safe: bool
    risk_level: str
    details: dict