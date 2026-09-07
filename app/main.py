from fastapi import FastAPI
from app.routers import recommendations

app = FastAPI(
    title="Recommendation Engine API",
    description="Integration layer for the GNN-based recommendation system (Person 4 scope).",
    version="1.0.0",
)

# Register routers
app.include_router(recommendations.router)


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}
