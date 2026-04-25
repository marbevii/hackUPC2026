from datetime import datetime

from flask import Flask, render_template, request

from services.ai_service import get_budget_destinations, get_destination_from_mood
from services.skyscanner_service import search_flights, search_flights_date_range

app = Flask(__name__)
app.secret_key = "hackupc_secret_key"


def get_mock_hotels(index):
    options = [
        [
            {"name": "Urban Nest Rooms", "price": 45, "address": "Central Avenue"},
            {"name": "Old Quarter Stay", "price": 75, "address": "Market Street"},
            {"name": "Skyline Boutique House", "price": 105, "address": "North Bridge Road"},
        ],
        [
            {"name": "River Corner Lodge", "price": 48, "address": "Riverside Walk"},
            {"name": "City Gate Hotel", "price": 82, "address": "Station Boulevard"},
            {"name": "Garden View Residence", "price": 112, "address": "Green Park Lane"},
        ],
        [
            {"name": "Metro Budget Inn", "price": 41, "address": "Main Square"},
            {"name": "Heritage Comfort Suites", "price": 78, "address": "Old Town Road"},
            {"name": "Panorama Design Rooms", "price": 118, "address": "Hilltop Avenue"},
        ],
    ]

    return options[index % len(options)]


def get_mock_restaurants(index):
    options = [
        [
            {"name": "Corner Market Bites", "price": 14, "address": "Food Market Lane"},
            {"name": "Local Table House", "price": 27, "address": "Old Centre Street"},
            {"name": "Evening Kitchen", "price": 39, "address": "Riverside Avenue"},
        ],
        [
            {"name": "Street Bowl Spot", "price": 12, "address": "South Market"},
            {"name": "Neighbourhood Grill", "price": 24, "address": "Liberty Street"},
            {"name": "Terrace Dinner Club", "price": 41, "address": "Upper District"},
        ],
        [
            {"name": "Daily Plate Café", "price": 15, "address": "Museum Road"},
            {"name": "Central Bistro", "price": 29, "address": "Main Boulevard"},
            {"name": "Night Garden Restaurant", "price": 44, "address": "Garden Walk"},
        ],
    ]

    return options[index % len(options)]


def get_mock_extras(index):
    options = [
        [
            {"name": "Historic Church Visit", "price": 10, "address": "Cathedral Square"},
            {"name": "Old City Guided Walk", "price": 35, "address": "Main Square"},
            {"name": "Mountain View Day Trip", "price": 60, "address": "Central Station"},
        ],
        [
            {"name": "Main Basilica Visit", "price": 12, "address": "Heritage Avenue"},
            {"name": "Cultural District Tour", "price": 32, "address": "Museum Quarter"},
            {"name": "Countryside Excursion", "price": 58, "address": "North Terminal"},
        ],
        [
            {"name": "Ancient Temple Visit", "price": 8, "address": "Old Town Gate"},
            {"name": "Local Guide City Tour", "price": 29, "address": "City Hall"},
            {"name": "Lake Region Day Trip", "price": 67, "address": "East Station"},
        ],
    ]

    return options[index % len(options)]


def normalize_travel_date(ai_data):
    date_was_provided = ai_data.get("date_was_provided", False)
    raw_date = ai_data.get("query_dates")

    if isinstance(raw_date, str):
        parts = raw_date.replace("-", "/").split("/")

        if len(parts) == 3:
            if len(parts[0]) == 4:
                return {
                    "year": int(parts[0]),
                    "month": int(parts[1]),
                    "day": int(parts[2])
                }

            return {
                "day": int(parts[0]),
                "month": int(parts[1]),
                "year": int(parts[2])
            }

    if date_was_provided and isinstance(raw_date, dict):
        return raw_date

    if isinstance(raw_date, dict):
        return raw_date

    now = datetime.now()
    month = now.month + 1
    year = now.year

    if month == 13:
        month = 1
        year += 1

    return {
        "year": year,
        "month": month,
        "day": 1
    }


def get_demo_fallback_flights(city_name):
    if city_name == "Bali":
        return [
            {
                "airline": "Vueling Airlines",
                "price": 461,
                "url": "https://www.skyscanner.es/transport/flights/bcn/dps/260615/"
            },
            {
                "airline": "Qatar Airways",
                "price": 837,
                "url": "https://www.skyscanner.es/transport/flights/bcn/dps/260615/"
            },
            {
                "airline": "Brussels Airlines",
                "price": 880,
                "url": "https://www.skyscanner.es/transport/flights/bcn/dps/260615/"
            }
        ]

    if city_name == "Amsterdam":
        return [
            {
                "airline": "Transavia",
                "price": 72,
                "url": "https://www.skyscanner.es/transport/flights/bcn/ams/260615/"
            },
            {
                "airline": "Vueling",
                "price": 89,
                "url": "https://www.skyscanner.es/transport/flights/bcn/ams/260615/"
            },
            {
                "airline": "KLM",
                "price": 145,
                "url": "https://www.skyscanner.es/transport/flights/bcn/ams/260615/"
            }
        ]

    return []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    mode = request.form.get("mode", "standard")

    if mode == "mood":
        images = request.files.getlist("images")
        ai_data = get_destination_from_mood(images)
        prompt_used = "Visual mood analysis"
        template_to_use = "budget_results_mood.html"
        use_date_range = False
    else:
        prompt = request.form.get("prompt", "")
        ai_data = get_budget_destinations(prompt)
        prompt_used = prompt
        template_to_use = "budget_results.html"
        use_date_range = True

    print("AI DATA:", ai_data)

    travel_date = normalize_travel_date(ai_data)
    budget = ai_data.get("budget", 999999)
    origin = ai_data.get("origin", "BCN")
    adults = ai_data.get("adult_count", 1)
    candidates = ai_data.get("candidate_destinations", ai_data.get("destinations", []))

    countries = []

    for destination in candidates:
        country_index = len(countries)
        city_name = destination.get("city")
        iata_code = destination.get("iata")

        if not city_name or not iata_code:
            continue

        try:
            if use_date_range:
                flights = search_flights_date_range(
                    origin,
                    iata_code,
                    travel_date,
                    adults,
                    days=7
                )
            else:
                flights = search_flights(
                    origin,
                    iata_code,
                    travel_date,
                    adults
                )
        except Exception as e:
            print(f"Flight search error for {city_name}: {e}")
            flights = []

        if not flights:
            flights = get_demo_fallback_flights(city_name)

        valid_flights = []

        for flight in flights:
            price = flight.get("price")

            try:
                price_number = float(price)
            except (TypeError, ValueError):
                continue

            if mode == "mood" or price_number <= budget:
                flight["price"] = price_number
                valid_flights.append(flight)

        if not valid_flights:
            continue

        valid_flights = sorted(valid_flights, key=lambda x: x["price"])[:3]

        country_data = {
            "country": destination.get("country", ""),
            "city": city_name,
            "reason": destination.get("reason", "Recommended destination based on your preferences."),
            "flights": valid_flights,
        }

        if mode != "mood":
            country_data.update({
                "hotels": get_mock_hotels(country_index),
                "food": get_mock_restaurants(country_index),
                "extras": get_mock_extras(country_index),
            })

        countries.append(country_data)

        if len(countries) == 3:
            break

    return render_template(
        template_to_use,
        prompt=prompt_used,
        countries=countries,
        travel_date=travel_date
    )


@app.route("/budget-results", methods=["POST"])
def budget_results():
    return search()


if __name__ == "__main__":
    app.run(debug=True, port=5050)