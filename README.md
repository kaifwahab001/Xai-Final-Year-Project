# Health Advice API

A Flask + scikit-learn API that accepts health metrics and returns personalised advice.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Service info |
| GET | `/health` | Health check (used by Render) |
| POST | `/predict` | Get prediction + advice |

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
