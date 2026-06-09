from fastapi import APIRouter
from app.schemas.url_check import URLRequest, URLCheckResponse
from app.services import google_sf_browsing, virustotal

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
    threat_type = vt.get("threat_type") or gsb.get("threat_type")

    # Ambos servicios fallaron
    if gsb_safe is None and vt_safe is None:
        return 50, "unknown", "unknown"

    # Un servicio falló → amarillo
    if gsb_safe is None or vt_safe is None:
        return 50, "suspicious", threat_type or "unknown"

    # Phishing/Social Engineering → siempre rojo
    if threat_type == "phishing":
        return 0, "phishing", "phishing"

    # Malware confirmado por cualquiera → rojo
    if threat_type == "malware" and (not gsb_safe or not vt_safe):
        return 0, "malware", "malware"

    # Unwanted software → amarillo
    if threat_type == "unwanted_software":
        return 33, "suspicious", "unwanted_software"

    # Ambos detectan amenaza → rojo
    if not gsb_safe and not vt_safe:
        return 0, "malicious", threat_type or "malicious"

    # Solo uno detecta amenaza → amarillo
    if not gsb_safe or not vt_safe:
        return 33, "suspicious", threat_type or "suspicious"

    # Solo engines sospechosos en VT (sin maliciosos)
    if vt_suspicious > 0:
        return 50, "suspicious", "suspicious"

    # Ambos dicen seguro → verde
    return 100, "safe", None

@router.post("/analyze", response_model=URLCheckResponse)
async def check_url(request: URLRequest):
    url = str(request.url)

    gsb_result = await google_sf_browsing.check(url)
    vt_result = await virustotal.check(url)

    score, risk_level, threat_type = _calculate_score_and_risk(gsb_result, vt_result)
    is_safe = score >= 67  # Verde = seguro

    return URLCheckResponse(
        url=url,
        score=score,
        is_safe=is_safe,
        risk_level=risk_level,
        threat_type=threat_type,
        details={
            "google_safe_browsing": gsb_result,
            "virustotal": vt_result
        }
    )