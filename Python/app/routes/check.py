from fastapi import APIRouter
from app.schemas.url_check import URLRequest, URLCheckResponse
from app.services import google_sf_browsing, virustotal, url_expander

router = APIRouter()

def _calculate_score_and_risk(gsb: dict, vt: dict) -> tuple[int, str, str]:
    """
    Retorna (score, risk_level, threat_type)
    Score: 0-100 donde 100 es más seguro
    """
    gsb_safe = gsb.get("is_safe")
    vt_safe = vt.get("is_safe")
    vt_malicious = vt.get("malicious_engines", 0)
    vt_suspicious = vt.get("suspicious_engines", 0)
    vt_total = vt.get("total_engines", 0)
    threat_type = vt.get("threat_type") or gsb.get("threat_type")
    if gsb_safe is None and vt_safe is None:
        return 50, "unknown", "unknown"
    if vt_safe is None and vt_total == 0 and gsb_safe is True:
        return 100, "safe", None

    if gsb_safe is None and vt_safe is True:
        return 100, "safe", None
    if gsb_safe is None or vt_safe is None:
        return 50, "suspicious", threat_type or "unknown"

    # Ambos dicen seguro → verde
    return 100, "safe", None

@router.post("/analyze", response_model=URLCheckResponse)
async def check_url(request: URLRequest):
    url = str(request.url)

    # Expandir si es un link acortado
    expanded_url = url
    was_expanded = False

    print(f"URL recibida: {url}")
    print(f"Is shortened: {url_expander.is_shortened(url)}")

    if url_expander.is_shortened(url):
        expanded_url = await url_expander.expand(url)
        was_expanded = expanded_url != url

    print(f"URL expandida: {expanded_url}")
    print(f"Was expanded: {was_expanded}")

    gsb_result = await google_sf_browsing.check(expanded_url)
    vt_result = await virustotal.check(expanded_url)

    score, risk_level, threat_type = _calculate_score_and_risk(gsb_result, vt_result)
    is_safe = score >= 67

    return URLCheckResponse(
        url=expanded_url,
        score=score,
        is_safe=is_safe,
        risk_level=risk_level,
        threat_type=threat_type,
        details={
            "original_url": url if was_expanded else None,
            "was_expanded": was_expanded,
            "google_safe_browsing": gsb_result,
            "virustotal": vt_result
        }
    )