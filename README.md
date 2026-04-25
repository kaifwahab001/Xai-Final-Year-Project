# Health Advice API

A Flask + scikit-learn API that accepts health metrics and returns personalised advice.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Service info |
| GET | `/health` | Health check (used by Render) |
| POST | `/predict` | Get prediction + advice |
| GET | `/all-data` | Get all historically saved predictions |
| GET | `/feature-data` | Get date-wise data for a specific feature |
| GET | `/heartbeats` | Get all historical heartbeat data |

### POST /predict – Request body

```json
{
  "heart_rate": 72,
  "steps": 8000,
  "sleep_hours": 7.5,
  "calories": 2200,
  "ambient_temp": 22
}
```

### POST /predict – Response

```json
{
  "input": { ... },
  "prediction": "0",
  "explanation": "Your heart rate is within a healthy range. ...",
  "advice": "Keep up your healthy heart habits! ..."
}
```

### GET /all-data – Response

```json
[
  {
    "id": 1,
    "timestamp": "2026-04-25T12:00:00.000000",
    "heart_rate": 72.0,
    "steps": 8000.0,
    "sleep_hours": 7.5,
    "calories": 2200.0,
    "ambient_temp": 22.0,
    "prediction": "0"
  }
]
```

### GET /feature-data – Request

**Query Parameters:**
- `feature` (required): The name of the feature to fetch (e.g., `Heart Rate`, `Steps`, `Sleep Hours`, `Calories`, `Ambient Temp`).

### GET /feature-data – Response

```json
{
  "feature": "Heart Rate",
  "data": [
    {
      "date": "2026-04-25T12:00:00.000000",
      "value": 72.0
    }
  ]
}
```

### GET /heartbeats – Response

```json
{
  "feature": "Heart Rate",
  "data": [
    {
      "date": "2026-04-25T12:00:00.000000",
      "value": 72.0
    }
  ]
}
```

---

## Deploy to Render (recommended – free tier)

1. Push this folder to a **GitHub repository**.
2. Go to [render.com](https://render.com) → **New → Web Service**.
3. Connect your GitHub repo.
4. Render auto-detects `render.yaml` – click **Deploy**.
5. Your API will be live at `https://<your-service>.onrender.com`.

> **Note:** Free-tier services on Render spin down after 15 min of inactivity. The first request after a cold start takes ~30 s.

---

## Deploy to Railway (alternative)

1. Install Railway CLI: `npm i -g @railway/cli`
2. `railway login && railway init && railway up`
3. Set the start command to: `gunicorn app:app --bind 0.0.0.0:$PORT`

---

## Run locally

```bash
pip install -r requirements.txt
python app.py
# API available at http://localhost:5000
```

Test with curl:

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"heart_rate":80,"steps":7000,"sleep_hours":7,"calories":2000,"ambient_temp":25}'
```
