import os
import json
import random
import logging

import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# ── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Paths (relative to this file so it works anywhere) ─────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
TEMPLATES_PATH = os.path.join(BASE_DIR, "templates_data", "templates.json")

# ── Load artefacts at startup (fail fast if files are missing) ─────────────
with open(os.path.join(MODEL_DIR, "metadata.json")) as f:
    metadata = json.load(f)

FEATURES = metadata["features"]
model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
logger.info("Model loaded. Features: %s", FEATURES)

with open(TEMPLATES_PATH) as f:
    templates = json.load(f)
logger.info("Templates loaded.")

# ── App ────────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)  # allow all origins; tighten in prod by passing origins=[...]


# ── Helper ─────────────────────────────────────────────────────────────────
def generate_detailed_advice(data: list) -> dict:
    hr, steps, sleep, calories, temp = data
    reasons, advice = [], []

    # Heart Rate
    if hr > 90:
        t = templates["heart_rate"]["high"]
    elif hr < 65:
        t = templates["heart_rate"]["low"]
    else:
        t = templates["heart_rate"]["normal"]
    reasons.append(random.choice(t["reasons"]))
    advice.append(random.choice(t["advice"]))

    # Steps
    if steps < 6000:
        t = templates["steps"]["low"]
    else:
        t = templates["steps"]["high"]
    reasons.append(random.choice(t["reasons"]))
    advice.append(random.choice(t["advice"]))

    # Sleep
    if sleep < 6.5:
        t = templates["sleep_hours"]["low"]
    else:
        t = templates["sleep_hours"]["high"]
    reasons.append(random.choice(t["reasons"]))
    advice.append(random.choice(t["advice"]))

    # Calories
    if "calories" in templates:
        if calories > 3000:
            t = templates["calories"]["high"]
        else:
            t = templates["calories"]["normal"]
        reasons.append(random.choice(t["reasons"]))
        advice.append(random.choice(t["advice"]))
    else:
        if calories > 3000:
            reasons.append("Your calorie intake is above average.")
            advice.append("Balance with light exercise.")
        else:
            reasons.append("Your calorie intake looks healthy.")
            advice.append("Keep up your balanced diet!")

    # Temperature
    if "ambient_temp" in templates:
        if temp > 30:
            t = templates["ambient_temp"]["high"]
        elif temp < 15:
            t = templates["ambient_temp"]["low"]
        else:
            t = templates["ambient_temp"]["normal"]
        reasons.append(random.choice(t["reasons"]))
        advice.append(random.choice(t["advice"]))
    else:
        if temp > 30:
            reasons.append("It's very hot outside.")
            advice.append("Stay hydrated and avoid heavy outdoor workouts.")
        elif temp < 15:
            reasons.append("It's cold outside.")
            advice.append("Dress warmly before any outdoor activity.")
        else:
            reasons.append("The temperature is comfortable.")
            advice.append("Great conditions for outdoor activity!")

    return {
        "summary": " ".join(reasons),
        "recommendations": " ".join(advice),
    }


# ── Routes ─────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Health Advice API",
        "status": "running",
        "endpoints": {
            "POST /predict": "Get health prediction and advice",
            "GET /health": "Health check"
        },
        "required_fields": FEATURES
    })


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Validate all required fields are present
    missing = [f for f in FEATURES if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        X = [float(data[f]) for f in FEATURES]
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"All fields must be numeric: {e}"}), 400

    X_input = pd.DataFrame([X], columns=FEATURES)
    prediction = model.predict(X_input)[0]
    detailed = generate_detailed_advice(X)

    logger.info("Prediction: %s | Input: %s", prediction, data)

    return jsonify({
        "input": data,
        "prediction": str(prediction),
        "explanation": detailed["summary"],
        "advice": detailed["recommendations"],
    })


# ── Entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
