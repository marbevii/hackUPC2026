from flask import Flask, render_template, request
from services.ai_service import get_budget_destinations
from services.skyscanner_service import search_flights

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/budget-results", methods=["POST"])
def budget_results():
    prompt = request.form.get("prompt", "")

    ai_data = get_budget_destinations(prompt)
    print("AI DATA:", ai_data)

    countries = []

    for destination in ai_data["destinations"]:
        countries.append({
            "country": destination["country"],
            "city": destination["city"],
            "reason": destination["reason"],

            "flights": search_flights(
                ai_data.get("origin", "BCN"),
                destination["iata"],
                ai_data.get("query_dates", {"year": 2026, "month": 6, "day": 15}),
                ai_data.get("adult_count", 1)
            ),

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

    return render_template(
        "budget_results.html",
        prompt=prompt,
        countries=countries,
        travel_date=ai_data.get("query_dates", {"day": 15, "month": 6, "year": 2026})
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
    app.run(debug=True)