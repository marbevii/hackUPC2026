from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/budget-results", methods=["POST"])
def budget_results():
    prompt = request.form.get("prompt", "")

    countries = [
        {
            "country": "Portugal",
            "city": "Lisbon",
            "reason": "Destí econòmic, bon clima, menjar assequible i vols freqüents.",
            "flights": [
                {"name": "Low Cost", "price": 85},
                {"name": "Directe Flexible", "price": 130},
                {"name": "Premium Horari Bo", "price": 180},
            ],
            "hotels": [
                {"name": "Hostel Centre", "price": 35},
                {"name": "Hotel 3★", "price": 70},
                {"name": "Apartment", "price": 95},
            ],
            "food": [
                {"name": "Street Food", "price": 18},
                {"name": "Restaurants locals", "price": 32},
                {"name": "Foodie plan", "price": 55},
            ],
            "extras": [
                {"name": "Transport públic", "price": 20},
                {"name": "Museus", "price": 25},
                {"name": "Excursió Sintra", "price": 45},
            ],
        }
    ]

    return render_template("budget_results.html", prompt=prompt, countries=countries)

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