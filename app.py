from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    mode = request.form.get("mode")

    if mode == "mood":
        images = request.files.getlist("images")
        return jsonify({
            "mode": mode,
            "message": f"S'han rebut {len(images)} imatges."
        })

    prompt = request.form.get("prompt")
    return jsonify({
        "mode": mode,
        "prompt": prompt,
        "message": "Prompt rebut correctament."
    })

@app.route("/results")
def results():
    return render_template("results.html")


if __name__ == "__main__":
    app.run(debug=True)