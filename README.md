# Recommendation Engine API (Integration + API + Evaluation)

FastAPI service that exposes the GNN recommendation pipeline (Person 1-3's work)
through a REST API, with Redis caching, Pytest tests, and MLflow tracking.

## Structure

```
recommendation-api/
├── app/
│   ├── main.py                    # FastAPI app entrypoint
│   ├── config.py                  # Settings (env-driven)
│   ├── schemas.py                 # Pydantic request/response models
│   ├── cache.py                   # Redis get/set helpers
│   ├── routers/
│   │   └── recommendations.py     # GET /recommendations/{user_id}
│   └── services/
│       └── recommender.py         # Integration point for Person 2/3's pipeline
├── tests/
│   └── test_recommendations.py    # Pytest suite
├── mlflow_tracking_example.py     # Example MLflow logging
├── requirements.txt
└── README.md
```

## Setup for Teammates (first time only)

### 1. Clone the repo
```bash
git clone https://github.com/shubhadipm49-pixel/recommendation-api.git
cd recommendation-api
```

### 2. Install Python 3.13 (if you don't already have it)
- **Mac (Homebrew):** `brew install python@3.13`
- **Windows:** download from python.org (3.11+ works fine)
- Check your version: `python3 --version`

### 3. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```
You should see `(venv)` appear at the start of your terminal prompt.

### 4. Install dependencies
```bash
python3 -m pip install -r requirements.txt
```

### 5. Install Docker Desktop (needed for Redis caching)
- Download from https://www.docker.com/products/docker-desktop/
- Install it, open the app once, and wait for it to fully start (whale icon in menu bar / system tray)

### 6. Start Redis
```bash
docker run -d -p 6379:6379 redis
```
Check it's running:
```bash
docker ps
```
You should see `redis` listed with status "Up."

### 7. Run the API
```bash
python3 -m uvicorn app.main:app --reload
```

### 8. Open the interactive docs
Go to: **http://127.0.0.1:8000/docs**

Try `GET /health` first (should return `{"status": "ok"}`), then try
`GET /recommendations/{user_id}` with any user_id (e.g. `U101`) — you'll get
mock recommendation data back. Run it twice with the same user_id and
`"cached"` should flip from `false` to `true`.

## Every time after the first setup

```bash
cd recommendation-api
source venv/bin/activate
docker run -d -p 6379:6379 redis   # skip if it says "port already allocated" — already running
python3 -m uvicorn app.main:app --reload
```
Then open http://127.0.0.1:8000/docs

## Run tests
```bash
pytest tests/ -v
```

## Next steps (as Person 2/3 finish their parts)

1. In `app/services/recommender.py`, replace the mock `get_recommendations`
   logic with real calls: load embeddings, query FAISS index, apply ranking.
2. Update `app/config.py` paths (`embeddings_path`, `faiss_index_path`) to
   point at the actual artifact files.
3. Once a trained model exists, log it via `mlflow_tracking_example.py`
   (swap in real params/metrics).
4. Add more test cases as edge cases come up (e.g., cold-start users with
   no interaction history).

## Notes on caching
- Cache key format: `rec:{user_id}`
- TTL: 5 minutes by default (`CACHE_TTL_SECONDS` in config)
- On cache hit, response includes `"cached": true` so you can verify it's working

## Troubleshooting

**"command not found: uvicorn" or "pip"**
Use `python3 -m` in front of the command instead:
```bash
python3 -m uvicorn app.main:app --reload
python3 -m pip install -r requirements.txt
```

**500 error when calling `/recommendations/{user_id}`**
Redis isn't running. Start it with `docker run -d -p 6379:6379 redis` and confirm with `docker ps`.

**"externally-managed-environment" error on pip install**
You're not inside the virtual environment. Run `source venv/bin/activate` first (confirm `(venv)` shows in your prompt), then retry.
