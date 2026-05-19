from fastapi import APIRouter
from app.schemas.url_check import URLRequest, URLCheckResponse
from app.services import google_sf_browsing, virustotal

router = APIRouter()

@router.post("/analyze", response_model=URLCheckResponse)
async def check_url(request: URLRequest):
    url = str(request.url)

    gsb_result = await google_sf_browsing.check(url)
    vt_result = await virustotal.check(url)

    # TODO: ajustar keys cuando implementemos los servicios reales
    is_safe = gsb_result["is_safe"] and vt_result["is_safe"]

    return URLCheckResponse(
        url=url,
        is_safe=is_safe,
        risk_level= "safe" if is_safe else "malicious", #TODO: add more risk levels
        details={"google_safe_browsing": gsb_result, "virustotal": vt_result} #TODO: add more details

    )