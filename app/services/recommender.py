"""
Integration layer between the API and the ML pipeline built by
Person 2 (GNN embeddings) and Person 3 (candidate generation + ranking).

Replace the TODOs below with real calls once their code/artifacts are ready.
Until then, this returns mock data so Person 4's API can be built and
tested independently.
"""

from typing import List
from app.schemas import RecommendedItem


class RecommenderService:
    def __init__(self):
        # TODO: load embeddings + FAISS index once available, e.g.:
        # self.embeddings = torch.load(settings.embeddings_path)
        # self.index = faiss.read_index(settings.faiss_index_path)
        self._loaded = False

    def get_recommendations(self, user_id: str, top_k: int = 20) -> List[RecommendedItem]:
        """
        Given a user_id, return top-k ranked recommendations.

        Real flow (once integrated):
          1. Look up user embedding
          2. Query FAISS index for top ~500 candidates (Person 3)
          3. Apply ranking model / filtering (Person 3)
          4. Return top_k items

        For now: mock data so the API contract is testable end-to-end.
        """
        mock_items = [
            RecommendedItem(product_id=f"P{1000 + i}", score=round(1.0 - i * 0.03, 4))
            for i in range(top_k)
        ]
        return mock_items


# Singleton instance reused across requests (avoids reloading model each call)
recommender_service = RecommenderService()
