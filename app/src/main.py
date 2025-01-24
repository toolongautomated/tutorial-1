from flask import Flask, jsonify, request

app = Flask(__name__)

PLANETS = {
    1: "Mercury",
    2: "Venus",
    3: "Earth",
    4: "Mars",
    5: "Jupiter",
    6: "Saturn",
    7: "Uranus",
    8: "Neptune",
}


@app.route("/")
def welcome():
    return "Welcome to the too long; automated app!"


@app.route("/planet")
def get_planet():
    try:
        position = int(request.args.get("position", 0))
        if position < 1:
            return jsonify({"error": "Position must be greater than 0"}), 400

        if position in PLANETS:
            return jsonify({"planet": PLANETS[position]}), 200

        return jsonify({"error": f"No planet exists at position {position}"}), 404

    except ValueError:
        return jsonify({"error": "Position must be a valid integer"}), 400


# No need to include app.run() here, as Gunicorn will handle running the app
