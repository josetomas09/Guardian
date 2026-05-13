# Guardian - Middleware de Seguridad para Adultos Mayores

**Guardian** es una web app pensada para ayudar a detectar posibles estafas digitales en adultos mayores. Su función es simple: analizamos mensajes sospechosos, interpretamos señales de riesgo y devolvemos un resultado claro, fácil de entender y accionable.

Trabajamos con un formato de semáforo para que el diagnóstico no quede en tecnicismos:

- **Verde**: el enlace parece seguro.
- **Amarillo**: hay señales raras o dudas razonables.
- **Rojo**: el riesgo es alto o la amenaza es probable.

---

## Descripción general

En el día a día, muchas estafas llegan por SMS, WhatsApp u otros mensajes que parecen legítimos. El problema es que no siempre es fácil detectar cuándo algo huele raro. Por eso planteamos **Guardian** como una herramienta intermedia: no reemplaza el criterio de la persona, pero sí le da una mano para decidir con más seguridad.

La propuesta apunta al área de un Proyecto de Extensión Comunitaria - SEC segurinfo - **Universidad Siglo 21** y busca combinar prevención, accesibilidad y educación digital. La idea es que cualquier usuario pueda copiar un mensaje, pegarlo en la app y obtener una guía clara sin tener que entender detalles técnicos complejos.

---

## Objetivo del proyecto

### Objetivo general
Desarrollar un sistema que analice mensajes sospechosos y entregue diagnósticos de riesgo mediante una interfaz sencilla, pensada especialmente para adultos mayores.

### Objetivos específicos
- Detectar URLs dentro de textos pegados por el usuario.
- Expandir enlaces acortados como `bit.ly`, `t.co` o `tinyurl`.
- Consultar servicios de reputación de forma asíncrona.
- Calcular un puntaje de riesgo entre 0 y 100.
- Mostrar el resultado con una interfaz accesible y de alto contraste.
- Incorporar material educativo con flashcards para concientización digital.

---

## Público objetivo

El sistema está orientado principalmente a **adultos mayores**, que muchas veces quedan más expuestos a:

- mensajes fraudulentos,
- premios falsos,
- urgencias inventadas,
- enlaces maliciosos,
- y pedidos de datos personales o credenciales.

Nuestra intención no es complicarles la experiencia, sino todo lo contrario: hacer que la respuesta sea clara, directa y útil. La idea va por ahí, bien al grano.

---

## Cómo funciona

Guardian actúa como un traductor de riesgos. En vez de mostrar datos técnicos difíciles de interpretar, convertimos esa información en una recomendación simple.

El flujo general es este:

1. La persona pega un mensaje sospechoso.
2. El sistema identifica URLs con expresiones regulares.
3. Se expanden enlaces acortados para conocer el destino real.
4. Se consultan motores de reputación de forma asíncrona.
5. Se calcula un score de riesgo.
6. Se presenta el resultado con un semáforo y un mensaje claro.
7. Se sugiere una acción concreta.

Además, cuidamos la privacidad: solo analizamos lo que la persona decide pegar manualmente. No interceptamos otras apps ni hacemos monitoreo en segundo plano.

---

## Arquitectura técnica

El proyecto se organiza con una arquitectura cliente-servidor bien separada:

### Frontend
- Aplicación web tipo SPA
- Enfoque mobile-first
- Interfaz simple y accesible
- Diseño centrado en claridad visual

### Backend
- Desarrollo en **Python**
- Uso de **FastAPI**
- Procesamiento asíncrono para consultas externas
- Lógica de scoring y orquestación del análisis

### Servicios externos
- **Google Safe Browsing API**
- **VirusTotal v3 API**

### Persistencia
- **SQLite** para configuración local y registros técnicos, cuando haga falta

### Infraestructura
- Despliegue posible en **Vercel** o **Render**
- Observabilidad básica para trazabilidad y monitoreo

---

## Requerimientos funcionales

- **RF-01:** cuadro de entrada de texto optimizado para copiar y pegar.
- **RF-02:** extracción automática de URLs.
- **RF-03:** expansión de enlaces acortados.
- **RF-04:** cálculo de riesgo con score de 0 a 100.
- **RF-05:** visualización del diagnóstico por colores.

---

## Requerimientos no funcionales

- **RNF-01 Usabilidad:** tipografía mayor a 18px y contraste mínimo 4.5:1.
- **RNF-02 Rendimiento:** latencia de diagnóstico menor a 3 segundos.
- **RNF-03 Seguridad:** comunicación bajo HTTPS/TLS 1.3 y autenticación mediante JWT.
- **RNF-04 Privacidad por diseño:** no persistir contenido sensible de los mensajes analizados.

---

## Especificaciones técnicas

### Backend
- Lenguaje: **Python**
- Framework: **FastAPI**
- Procesamiento: tareas asíncronas
- Respuesta: JSON

### Frontend
- Framework sugerido: **React**
- Interfaz responsive
- Componentes accesibles
- Prioridad en legibilidad y uso simple

### Integraciones
- Google Safe Browsing para detección de URLs peligrosas
- VirusTotal v3 para análisis y reputación adicional

### Algoritmo de scoring
El puntaje de riesgo puede considerar:

- longitud de la URL,
- entropía de caracteres,
- palabras asociadas a urgencia,
- uso de acortadores,
- resultados de reputación externa,
- patrones típicos de phishing.

---

## Casos de prueba

| ID | Caso de prueba | Entrada | Resultado esperado |
|---|---|---|---|
| CP-01 | URL legítima | `Accede a google.com` | Verde: "Enlace seguro. Puede continuar." |
| CP-02 | Phishing confirmado | `Actualiza tu clave: bit.ly/malicious` | Rojo: "Peligro. Amenaza detectada. No abra el enlace." |
| CP-03 | URL sospechosa | `Gana un premio: t.co/xyz123` | Amarillo: "Precaución. El destino es incierto o redirecciona." |
| CP-04 | Texto sin links | `Hola, ¿cómo estás?` | Informativo: "No se detectaron enlaces para analizar." |

---

## Interfaz propuesta

### Pantalla de inicio
- Diseño limpio y minimalista
- Área central para pegar texto
- Acceso rápido al análisis

### Pantalla de resultado
- Indicador visual bien destacado
- Mensaje corto y directo
- Recomendación concreta para seguir o no seguir el enlace

### Sección de concientización
- Flashcards con ejemplos reales o simulados de fraude
- Contenido educativo para reforzar hábitos seguros
- Lenguaje simple y cercano

---

## Seguridad y privacidad

Guardian fue pensado con un enfoque de privacidad por diseño. Eso implica que:

- no capturamos datos de otras aplicaciones,
- no actuamos como bloqueador automático,
- no persistimos mensajes privados después del análisis,
- y solo usamos la información que el usuario decide enviar.

Con esto buscamos reducir riesgos, cuidar recursos y mantener una experiencia más confiable.

---

## Alcance del sistema

### Incluye
- análisis de mensajes y URLs,
- expansión de enlaces acortados,
- diagnóstico por colores,
- recomendaciones de acción,
- módulo educativo básico.

### No incluye
- protección contra vishing,
- filtrado en tiempo real del sistema operativo,
- monitoreo de tráfico de red de otras aplicaciones.

---

## Stack tecnológico propuesto

- **Frontend:** React
- **Backend:** FastAPI
- **APIs de seguridad:** Google Safe Browsing, VirusTotal v3
- **Base de datos:** SQLite
- **Autenticación:** JWT
- **Transporte seguro:** HTTPS / TLS 1.3
- **Despliegue:** Vercel / Render

---

## Referencias

- Google Safe Browsing API  
  https://developers.google.com/safe-browsing

- VirusTotal API v3  
  https://developers.virustotal.com/reference

- OWASP Top 10  
  https://owasp.org/www-project-top-ten/

---


---

## Cierre

Este proyecto fue pensado como una propuesta mediática y educativa para ayudar a prevenir estafas digitales en adultos mayores, con un enfoque claro, accesible y práctico.
