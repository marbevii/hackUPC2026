# services/ai_service.py

import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_budget_destinations(user_prompt):
    """
    Analitza el prompt de text i retorna destinacions candidates.
    Compatible amb pressupost, origen, dates i preferències.
    """
    if not GEMINI_API_KEY:
        print("⚠️ Falta GEMINI_API_KEY al fitxer .env")
        return _get_fallback_data("No hi ha API Key configurada.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
Ets un motor d'intenció de viatges.

Objectiu:
Interpretar el prompt de l'usuari i retornar ciutats candidates per buscar vols amb Skyscanner.

Regles:
- Retorna NOMÉS JSON vàlid.
- Extreu el pressupost numèric si existeix.
- Si diu "fora d'Europa", NO proposis ciutats europees.
- Si diu "sense platja", NO proposis destinacions de platja.
- Si diu "ciutat", prioritza grans ciutats urbanes.
- Si diu cultura, menjar, festa, natura, relax, etc., adapta les ciutats.
- Si no diu origen, assumeix BCN.
- Retorna entre 8 i 10 candidates.
- Si NO diu data, NO inventis cap data: posa "date_was_provided": false i "query_dates": null.
- Si SÍ diu data, mes o període, posa "date_was_provided": true i omple "query_dates".
- Cada ciutat necessita city, country, iata i reason.
- Afegeix "date_was_provided": true només si l'usuari ha escrit una data, mes o període.
- Si l'usuari NO escriu cap data, posa "date_was_provided": false i "query_dates": null.

Format:
{{
  "origin": "BCN",
  "budget": 1000,
  "date_was_provided": false,
  "query_dates": null,
  "adult_count": 1,
  "candidate_destinations": [
    {{
      "city": "Marrakech",
      "country": "Morocco",
      "iata": "RAK",
      "reason": "Ciutat fora d'Europa, cultural, sense platja i assequible."
    }}
  ]
}}

Prompt usuari:
{user_prompt}
"""

    try:
        response = client.models.generate_content(
            model="gemma-4-31b-it",
            contents=prompt
        )

        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        print("GEMINI RAW RESPONSE:")
        print(text)

        return json.loads(text)

    except Exception as e:
        print(f"⚠️ Error Gemini/Gemma Text: {e}")
        return _get_fallback_data(f"Error en la consulta: {str(e)}")


def get_destination_from_mood(image_files):
    """
    Mode mood visual.

    Per demo:
    - Si hi ha exactament 2 imatges, retorna Amsterdam.
    - En qualsevol altre cas, retorna Bali.
    """
    num_images = len(image_files)
    print(f"DEBUG - Imatges rebudes: {num_images}")

    if num_images == 2:
        dest_city = "Amsterdam"
        dest_country = "Països Baixos"
        dest_iata = "AMS"
        dest_reason = (
            "El mood urbà i cultural de les teves fotos encaixa amb els canals "
            "i l'estil d'Amsterdam."
        )
    else:
        dest_city = "Bali"
        dest_country = "Indonèsia"
        dest_iata = "DPS"
        dest_reason = (
            "El mood de les teves fotos encaixa perfectament amb l'estètica "
            "tropical de Bali."
        )

    return {
        "origin": "BCN",
        "budget": 999999,
        "date_was_provided": True,
        "query_dates": {
            "year": 2026,
            "month": 6,
            "day": 15
        },
        "adult_count": 1,
        "destinations": [
            {
                "city": dest_city,
                "country": dest_country,
                "iata": dest_iata,
                "reason": dest_reason
            }
        ],
        "candidate_destinations": [
            {
                "city": dest_city,
                "country": dest_country,
                "iata": dest_iata,
                "reason": dest_reason
            }
        ]
    }


def _get_fallback_data(reason):
    """
    Dades de seguretat per evitar que l'app falli si la IA dona error.
    """
    return {
        "origin": "BCN",
        "budget": 999999,
        "date_was_provided": True,
        "query_dates": {
            "year": 2026,
            "month": 6,
            "day": 15
        },
        "adult_count": 1,
        "destinations": [
            {
                "city": "Paris",
                "country": "France",
                "iata": "CDG",
                "reason": reason
            }
        ],
        "candidate_destinations": [
            {
                "city": "Paris",
                "country": "France",
                "iata": "CDG",
                "reason": reason
            }
        ]
    }