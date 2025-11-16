# app/ai_service.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    # No lanzamos excepción en import time para permitir levantar la app sin la key,
    # pero las funciones que necesiten la key validan y retornan error claro.
    genai_configured = False
else:
    genai.configure(api_key=GEMINI_API_KEY)
    genai_configured = True


def generate_post(prompt: str):
    """
    Genera título, cuerpo y seo usando gemini-2.5-flash.
    Lanza Exception si la generación falla o no está configurada la API key.
    """
    if not genai_configured:
        raise RuntimeError("GEMINI_API_KEY no configurada. Añade GEMINI_API_KEY en .env para usar IA.")

    # Usamos explicitamente gemini-2.5-flash tal como lo especificaste
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Llamada sencilla. Ajusta los parámetros del modelo según tu necesidad (temperature, maxTokens, etc.)
    response = model.generate_content(
        f"Genera un artículo de blog con título, cuerpo y SEO sobre: {prompt}"
    )

    # response.text podría tener distintos formatos; lo manejamos con tolerancia
    text = getattr(response, "text", "") or ""
    if not text:
        # intenta obtener contenido en otras formas (estructura depende de la SDK/version)
        try:
            # algunas versiones devuelven choices[0].content
            text = response.choices[0].content
        except Exception:
            raise RuntimeError("Respuesta vacía de Gemini.")

    # Intentamos separar: Título, SEO (opcional) y cuerpo.
    parts = text.split("\n\n")
    title = parts[0].replace("Título:", "").strip() if len(parts) >= 1 else "Artículo sin título"
    seo = ""
    body = ""

    # Busca secciones que empiecen con "SEO:" o "SEO" en la segunda parte
    if len(parts) == 1:
        body = parts[0]
    elif len(parts) == 2:
        # no sabemos si es SEO o cuerpo; asumimos que la segunda es el cuerpo
        body = parts[1]
    else:
        # 3+ partes: asumimos [title, seo?, body...]
        # si la segunda empieza por "SEO", la tomamos como seo
        if parts[1].strip().lower().startswith("seo"):
            seo = parts[1].replace("SEO:", "").replace("SEO", "").strip()
            body = "\n\n".join(parts[2:])
        else:
            body = "\n\n".join(parts[1:])

    return title, body, seo
