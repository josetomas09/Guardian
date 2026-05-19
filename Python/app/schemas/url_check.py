from pydantic import BaseModel, HttpUrl

class URLRequest(BaseModel):
    url: HttpUrl

class URLCheckResponse(BaseModel):
    url: str
    is_safe: bool
    risk_level: str
    details: str