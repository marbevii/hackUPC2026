# services/ai_service.py

import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_budget_destinations(user_prompt):
    if not GEMINI_API_KEY:
        raise Exception("Falta GEMINI_API_KEY al fitxer .env")

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
- Retorna entre 8 i 10 candidates, no només 3.
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

    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=prompt
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    print("GEMINI RAW RESPONSE:")
    print(text)

    return json.loads(text)