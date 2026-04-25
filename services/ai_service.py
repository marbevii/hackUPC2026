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
Ets un expert en recomanació de viatges.

Interpreta EXACTAMENT el que demana l'usuari i proposa 3 ciutats que encaixin.

Regles:
- Si diu "sense platja", NO proposis ciutats de platja.
- Si diu "ciutat", prioritza ciutats urbanes.
- Si diu "menys de X euros", prioritza opcions assequibles.
- Si diu "cultura", prioritza museus, història, gastronomia i ambient urbà.
- Si no diu origen, assumeix BCN.
- Si no diu data, usa 15/6/2026.
- Retorna NOMÉS JSON vàlid.
- Retorna EXACTAMENT 3 destinacions.
- Cada destinació ha de tenir city, country, iata i reason.

Format:
{{
  "origin": "BCN",
  "query_dates": {{"year": 2026, "month": 6, "day": 15}},
  "adult_count": 1,
  "destinations": [
    {{
      "city": "Madrid",
      "country": "Spain",
      "iata": "MAD",
      "reason": "Ciutat urbana, sense platja, cultural i adequada pel pressupost."
    }},
    {{
      "city": "Prague",
      "country": "Czech Republic",
      "iata": "PRG",
      "reason": "Ciutat cultural, assequible, urbana i sense platja."
    }},
    {{
      "city": "Vienna",
      "country": "Austria",
      "iata": "VIE",
      "reason": "Ciutat urbana, cultural, sense platja i amb molt bona gastronomia."
    }}
  ]
}}

Prompt usuari:
{user_prompt}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    print("GEMINI RAW RESPONSE:")
    print(text)

    return json.loads(text)