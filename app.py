from flask import Flask, render_template, request
from services.ai_service import get_budget_destinations
from services.skyscanner_service import search_flights_date_range
from datetime import datetime

app = Flask(__name__)

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


@app.route("/")
def home():
    return render_template("index.html")


def normalize_travel_date(ai_data):
    date_was_provided = ai_data.get("date_was_provided", False)
    raw_date = ai_data.get("query_dates")

    if isinstance(raw_date, str):
        parts = raw_date.replace("-", "/").split("/")

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


@app.route("/budget-results", methods=["POST"])
def budget_results():
    prompt = request.form.get("prompt", "")

    ai_data = get_budget_destinations(prompt)
    print("AI DATA:", ai_data)

    travel_date = normalize_travel_date(ai_data)

    budget = ai_data.get("budget", 999999)
    origin = ai_data.get("origin", "BCN")
    adults = ai_data.get("adult_count", 1)

    candidates = ai_data.get("candidate_destinations", ai_data.get("destinations", []))
    countries = []

    for destination in candidates:
        country_index = len(countries)

        flights = search_flights_date_range(
            origin,
            destination["iata"],
            travel_date,
            adults,
            days=7
        )

        valid_flights = []

        for flight in flights:
            price = flight.get("price")

            if isinstance(price, (int, float)) and price <= budget:
                valid_flights.append(flight)

        if not valid_flights:
            continue

        valid_flights = sorted(valid_flights, key=lambda x: x["price"])[:3]

        countries.append({
            "country": destination["country"],
            "city": destination["city"],
            "reason": destination["reason"],
            "flights": valid_flights,
            "hotels": get_mock_hotels(country_index),
            "food": get_mock_restaurants(country_index),
            "extras": get_mock_extras(country_index),
        })

        if len(countries) == 5:
            break

    return render_template(
        "budget_results.html",
        prompt=prompt,
        countries=countries,
        travel_date=travel_date
    )


@app.route("/search", methods=["POST"])
def search():
    mode = request.form.get("mode", "")
    prompt = request.form.get("prompt", "")

    if mode == "mood":
        images = request.files.getlist("images")
        return {
            "mode": mode,
            "message": f"S'han rebut {len(images)} imatges.",
            "prompt": ""
        }

    return {
        "mode": mode,
        "message": "Prompt rebut correctament.",
        "prompt": prompt
    }


if __name__ == "__main__":
    app.run(debug=True, port=5050)