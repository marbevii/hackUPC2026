from flask import Flask, render_template, request
from services.ai_service import get_budget_destinations
from services.skyscanner_service import search_flights_date_range
from datetime import datetime

app = Flask(__name__)


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
            "hotels": [
                {"name": "Hostel", "price": 35},
                {"name": "Hotel 3★", "price": 70},
                {"name": "Apartment", "price": 95},
            ],
            "food": [
                {"name": "Low budget", "price": 18},
                {"name": "Local food", "price": 32},
                {"name": "Foodie plan", "price": 55},
            ],
            "extras": [
                {"name": "Transport públic", "price": 20},
                {"name": "Museus / activitats", "price": 25},
                {"name": "Excursió", "price": 45},
            ],
        })

        if len(countries) == 3:
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