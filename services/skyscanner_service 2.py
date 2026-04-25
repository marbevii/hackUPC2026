import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

SKYSCANNER_API_KEY = os.getenv("SKYSCANNER_API_KEY")

CREATE_URL = "https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create"
POLL_URL = "https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/poll"


def get_mock_flights(destination_iata):
    return [
        {"name": f"No real flights parsed · {destination_iata}", "price": "-"},
        {"name": "Check terminal Skyscanner response", "price": "-"},
        {"name": "Fallback active", "price": "-"},
    ]


def search_flights(origin_iata, destination_iata, date, adults=1):
    print("\n--- SKYSCANNER SEARCH ---")
    print("Origin:", origin_iata)
    print("Destination:", destination_iata)
    print("Date:", date)

    if not SKYSCANNER_API_KEY:
        print("No SKYSCANNER_API_KEY found.")
        return get_mock_flights(destination_iata)

    headers = {
        "x-api-key": SKYSCANNER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "query": {
            "market": "ES",
            "locale": "es-ES",
            "currency": "EUR",
            "queryLegs": [
                {
                    "originPlaceId": {"iata": origin_iata},
                    "destinationPlaceId": {"iata": destination_iata},
                    "date": {
                        "year": date.get("year", 2026),
                        "month": date.get("month", 6),
                        "day": date.get("day", 15)
                    }
                }
            ],
            "adults": adults,
            "cabinClass": "CABIN_CLASS_ECONOMY"
        }
    }

    try:
        create_response = requests.post(
            CREATE_URL,
            headers=headers,
            json=payload,
            timeout=20
        )

        print("CREATE STATUS:", create_response.status_code)
        create_response.raise_for_status()

        create_data = create_response.json()
        print("CREATE KEYS:", create_data.keys())

        session_token = create_data.get("sessionToken")

        if not session_token:
            print("No sessionToken.")
            print("CREATE DATA:", create_data)
            return get_mock_flights(destination_iata)

        poll_data = None

        for attempt in range(5):
            print(f"POLL ATTEMPT {attempt + 1}")

            poll_response = requests.post(
                f"{POLL_URL}/{session_token}",
                headers=headers,
                timeout=20
            )

            print("POLL STATUS:", poll_response.status_code)
            poll_response.raise_for_status()

            poll_data = poll_response.json()

            status = poll_data.get("status")
            action = poll_data.get("action")

            print("POLL STATUS FIELD:", status)
            print("POLL ACTION FIELD:", action)

            results = poll_data.get("content", {}).get("results", {})
            print("RESULT KEYS:", results.keys())

            flights = parse_flights(poll_data, origin_iata, destination_iata)

            if flights:
                return flights

            time.sleep(2)

        print("FINAL POLL DATA:", poll_data)
        return get_mock_flights(destination_iata)

    except Exception as e:
        print("Skyscanner error:", e)
        return get_mock_flights(destination_iata)


def clean_price(raw_price):
    price = float(raw_price)

    if price > 100000:
        price = price / 1000
    elif price > 10000:
        price = price / 100

    price = round(price)

    if price < 15 or price > 900:
        return None

    return price


def parse_time(value):
    if not value:
        return ""

    if isinstance(value, dict):
        hour = value.get("hour")
        minute = value.get("minute")
        if hour is not None and minute is not None:
            return f"{int(hour):02d}:{int(minute):02d}"

    if isinstance(value, str) and "T" in value:
        return value.split("T")[1][:5]

    return ""


def parse_flights(data, origin_iata, destination_iata):
    results = data.get("content", {}).get("results", {})

    itineraries = results.get("itineraries", {})
    legs = results.get("legs", {})
    carriers = results.get("carriers", {})

    if not itineraries:
        return []

    flights = []

    for itinerary_id, itinerary in itineraries.items():
        pricing_options = itinerary.get("pricingOptions", [])

        if not pricing_options:
            continue

        raw_price = pricing_options[0].get("price", {}).get("amount")

        if raw_price is None:
            continue

        price = clean_price(raw_price)

        if price is None:
            continue

        leg_ids = itinerary.get("legIds", [])
        airline_name = "Companyia"
        departure_time = ""

        if leg_ids:
            leg = legs.get(leg_ids[0], {})

            departure_time = parse_time(
                leg.get("departureDateTime")
                or leg.get("departure")
                or leg.get("localDepartureDateTime")
            )

            carrier_ids = (
                leg.get("marketingCarrierIds")
                or leg.get("operatingCarrierIds")
                or leg.get("carrierIds")
                or []
            )

            if carrier_ids:
                carrier = carriers.get(carrier_ids[0], {})
                airline_name = (
                    carrier.get("name")
                    or carrier.get("displayCode")
                    or carrier.get("iata")
                    or "Companyia"
                )

        label = airline_name

        if departure_time:
            label += f" · {departure_time}"

        flights.append({
            "name": label,
            "price": price
        })

        if len(flights) == 3:
            break

    print("PARSED FLIGHTS:", flights)
    return flights