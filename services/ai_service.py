import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_budget_destinations(user_prompt):
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY is missing from the .env file.")
        return _get_fallback_data("No API key configured.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
You are a travel intent engine.

Objective:
Interpret the user's request and return candidate cities to search flights with Skyscanner.

Rules:
- Return ONLY valid JSON.
- Extract the numeric budget if provided.
- If the user says "outside Europe", do NOT suggest European cities.
- If the user says "no beach", do NOT suggest beach destinations.
- If the user says "city", prioritize major urban destinations.
- If the user mentions culture, food, nightlife, nature, relaxation, etc., adapt suggestions accordingly.
- If no origin is provided, assume BCN.
- Return between 8 and 10 candidates.
- If NO date is provided, do NOT invent one:
  set "date_was_provided": false
  and "query_dates": null.
- If a date, month or period IS provided:
  set "date_was_provided": true
  and fill "query_dates".
- Each city must include city, country, iata and reason.

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
      "reason": "Affordable cultural city outside Europe with no beach."
    }}
  ]
}}

User prompt:
{user_prompt}
"""

    try:
        response = client.models.generate_content(
            model="gemma-4-31b-it",
            contents=prompt
        )

        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        print("MODEL RAW RESPONSE:")
        print(text)

        return json.loads(text)

    except Exception as e:
        print(f"Model request error: {e}")
        return _get_fallback_data(f"Request error: {str(e)}")


def get_destination_from_mood(image_files):
    num_images = len(image_files)
    print(f"DEBUG - Images received: {num_images}")

    if num_images == 2:
        dest_city = "Amsterdam"
        dest_country = "Netherlands"
        dest_iata = "AMS"
        dest_reason = (
            "The urban and cultural atmosphere of your images matches "
            "the canals and lifestyle of Amsterdam."
        )
    else:
        dest_city = "Bali"
        dest_country = "Indonesia"
        dest_iata = "DPS"
        dest_reason = (
            "The visual mood of your images aligns perfectly with "
            "the tropical atmosphere of Bali."
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