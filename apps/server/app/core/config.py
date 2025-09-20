from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+psycopg://fashion3d:fashion3d@localhost:5432/fashion3d"
    redis_url: str = "redis://localhost:6379/0"
    minio_endpoint: str = "http://localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket_raw: str = "raw-videos"
    minio_bucket_artifacts: str = "artifacts"
    jwt_secret: str = "devsecret"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24
    stripe_webhook_secret: str = "whsec_dummy"
    worker_webhook_secret: str = "workersecret"
    prometheus_port: int = 8001
    rate_free_scans: int = 3
    environment: Literal["development", "production", "test"] = "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
