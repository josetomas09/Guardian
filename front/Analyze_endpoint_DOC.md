# Guardian API — Documentación de Respuesta

## Endpoint

```
POST /api/v1/analyze
Content-Type: application/json
```

### Request
```json
{
  "url": "https://sitio-sospechoso.com"
}
```

---

## Respuesta completa

```json
{
  "url": "http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/MALWARE/URL/",
  "score": 0,
  "is_safe": false,
  "risk_level": "malware",
  "threat_type": "malware",
  "details": {
    "original_url": null,
    "was_expanded": false,
    "google_safe_browsing": {
      "is_safe": true,
      "threats": []
    },
    "virustotal": {
      "is_safe": false,
      "malicious_engines": 8,
      "suspicious_engines": 1,
      "total_engines": 92,
      "threat_type": "malware",
      "categories": {
        "alphaMountain.ai": "Information Technology, Suspicious",
        "Webroot": "Phishing and Other Frauds"
      }
    }
  }
}
```

---

## Campos principales

| Campo | Tipo | Descripción |
|---|---|---|
| `url` | `string` | URL analizada. Si era un link acortado, esta es la URL destino real. |
| `score` | `int` | Puntaje de seguridad de 0 a 100. **100 = seguro, 0 = peligroso.** |
| `is_safe` | `bool` | `true` si el score es ≥ 67 (verde). `false` si es amarillo o rojo. |
| `risk_level` | `string` | Nivel de riesgo. Ver tabla de valores posibles abajo. |
| `threat_type` | `string \| null` | Tipo de amenaza detectada. `null` si la URL es segura. |

---

## Valores de `risk_level`

| Valor | Color semáforo | Score | Descripción |
|---|---|---|---|
| `"safe"` | 🟢 Verde | 100 | Ningún servicio detectó amenazas. |
| `"suspicious"` | 🟡 Amarillo | 33–50 | Solo un servicio detectó algo, o la amenaza es leve. |
| `"malware"` | 🔴 Rojo | 0 | Detectado como malware por uno o ambos servicios. |
| `"phishing"` | 🔴 Rojo | 0 | Detectado como phishing o ingeniería social. |
| `"malicious"` | 🔴 Rojo | 0 | Ambos servicios lo marcan como peligroso (tipo genérico). |
| `"unknown"` | 🟡 Amarillo | 50 | Uno o ambos servicios fallaron. No se pudo verificar. |

---

## Valores de `threat_type`

| Valor | Descripción |
|---|---|
| `"malware"` | Software malicioso, virus, troyano, ransomware. |
| `"phishing"` | Intento de robo de datos personales o credenciales. |
| `"unwanted_software"` | Software no deseado, adware, PUP. |
| `"suspicious"` | Comportamiento sospechoso sin clasificación exacta. |
| `"malicious"` | Marcado como malicioso sin tipo específico. |
| `"unknown"` | No se pudo determinar el tipo (servicio caído o URL desconocida). |
| `null` | URL segura, sin amenazas detectadas. |

---

## Campo `details`

Contiene el desglose técnico de cada servicio. Útil para mostrar información adicional en la UI.

### `details.original_url`
- `string` si la URL fue expandida (era un link acortado como bit.ly)
- `null` si la URL no era un link acortado

### `details.was_expanded`
- `true` si la URL original era un link acortado y fue expandida antes del análisis
- `false` en caso contrario

### `details.google_safe_browsing`

| Campo | Tipo | Descripción |
|---|---|---|
| `is_safe` | `bool \| null` | `true` si no detectó amenazas. `null` si el servicio falló. |
| `threats` | `array` | Lista de hashes de amenazas detectadas. Vacío si es segura. |

### `details.virustotal`

| Campo | Tipo | Descripción |
|---|---|---|
| `is_safe` | `bool \| null` | `true` si 0 motores detectaron amenazas. `null` si el servicio falló. |
| `malicious_engines` | `int` | Cantidad de motores que marcaron la URL como maliciosa. |
| `suspicious_engines` | `int` | Cantidad de motores que marcaron la URL como sospechosa. |
| `total_engines` | `int` | Total de motores que analizaron la URL. |
| `threat_type` | `string \| null` | Tipo de amenaza según VirusTotal. |
| `categories` | `object` | Categorías asignadas por distintos servicios de seguridad. Clave = nombre del servicio, valor = categoría asignada. |

---

## Lógica del semáforo (resumen para el frontend)

```
score == 100              → 🟢 Verde  → "Enlace seguro"
score >= 33 && score < 67 → 🟡 Amarillo → "Precaución"
score < 33                → 🔴 Rojo   → "Peligro"
```

El campo `risk_level` ya viene procesado — el frontend puede usarlo directamente sin recalcular nada.

---

## Casos especiales

### Link acortado (bit.ly, t.co, etc.)
Cuando `was_expanded: true`, el campo `url` contiene la URL destino real y `original_url` contiene el link acortado original. El frontend puede mostrar ambas para mayor transparencia.

```json
{
  "url": "https://sitio-peligroso.com",
  "details": {
    "original_url": "https://bit.ly/xyz123",
    "was_expanded": true
  }
}
```

### Servicio caído
Cuando un servicio falla, su campo `is_safe` vale `null` y aparece un campo `error` con la descripción del problema. El score baja a 50 (amarillo) por precaución.

```json
{
  "score": 50,
  "risk_level": "unknown",
  "details": {
    "google_safe_browsing": {
      "is_safe": null,
      "error": "No se pudo conectar con Google Safe Browsing"
    }
  }
}
```

### URL no encontrada en bases de datos
Si VirusTotal nunca analizó la URL, devuelve `total_engines: 0`. El score es 50 por precaución.

```json
{
  "score": 50,
  "details": {
    "virustotal": {
      "is_safe": null,
      "malicious_engines": 0,
      "total_engines": 0
    }
  }
}
```
