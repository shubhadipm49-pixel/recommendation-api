import json
import redis
from app.config import settings

# Single shared Redis connection pool for the app
redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    decode_responses=True,
)


def get_cached_recommendations(user_id: str):
    """Return cached recommendation list for a user, or None if not cached."""
    key = f"rec:{user_id}"
    raw = redis_client.get(key)
    if raw is None:
        return None
    return json.loads(raw)


def set_cached_recommendations(user_id: str, items: list):
    """Cache recommendation list for a user with a TTL."""
    key = f"rec:{user_id}"
    redis_client.set(key, json.dumps(items), ex=settings.cache_ttl_seconds)
