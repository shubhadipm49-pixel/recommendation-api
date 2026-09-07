from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Centralized app configuration.
    Values can be overridden via environment variables or a .env file.
    """
    app_name: str = "Recommendation Engine API"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    cache_ttl_seconds: int = 300  # 5 minutes

    top_k: int = 20  # number of items to return per recommendation request

    # Path to artifacts produced by Person 1/2/3 (embeddings, index, model)
    embeddings_path: str = "artifacts/embeddings.pt"
    faiss_index_path: str = "artifacts/index.faiss"

    class Config:
        env_file = ".env"


settings = Settings()
