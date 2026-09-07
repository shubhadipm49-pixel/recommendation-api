from pydantic import BaseModel, Field  # type: ignore[reportMissingImports]
from typing import List


class RecommendedItem(BaseModel):
    product_id: str
    score: float = Field(..., description="Ranking score assigned by the ranker")


class RecommendationResponse(BaseModel):
    user_id: str
    items: List[RecommendedItem]
    cached: bool = Field(default=False, description="Whether this response was served from cache")


class ErrorResponse(BaseModel):
    detail: str
