# Recommendation Engine API (Person 4 — Integration + API + Evaluation)

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

## Setup

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

You'll also need Redis running locally (or update `REDIS_HOST`/`REDIS_PORT` env vars):

```bash
# via Docker, easiest option:
docker run -d -p 6379:6379 redis
```

## Run the API

```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI.

Test the endpoint:
```bash
curl http://127.0.0.1:8000/recommendations/U101
```

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
