from fastapi import APIRouter, HTTPException
from app.schemas import RecommendationResponse, RecommendedItem
from app.services.recommender import recommender_service
from app.cache import get_cached_recommendations, set_cached_recommendations
from app.config import settings

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/{user_id}", response_model=RecommendationResponse)
def get_recommendations(user_id: str):
    if not user_id.strip():
        raise HTTPException(status_code=400, detail="user_id must not be empty")

    # 1. Check cache first
    cached = get_cached_recommendations(user_id)
    if cached is not None:
        return RecommendationResponse(
            user_id=user_id,
            items=[RecommendedItem(**item) for item in cached],
            cached=True,
        )

    # 2. Cache miss -> run pipeline (candidate generation + ranking)
    items = recommender_service.get_recommendations(user_id, top_k=settings.top_k)

    if not items:
        raise HTTPException(status_code=404, detail=f"No recommendations found for user {user_id}")

    # 3. Store in cache for next time
    set_cached_recommendations(user_id, [item.model_dump() for item in items])

    return RecommendationResponse(user_id=user_id, items=items, cached=False)
