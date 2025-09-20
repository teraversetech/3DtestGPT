from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
    minio_access_key: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    minio_secret_key: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    minio_bucket_raw: str = os.getenv("MINIO_BUCKET_RAW", "raw-videos")
    minio_bucket_artifacts: str = os.getenv("MINIO_BUCKET_ARTIFACTS", "artifacts")
    gpu_enabled: bool = os.getenv("GPU_ENABLED", "false").lower() == "true"
    low_quality_mode: bool = os.getenv("LOW_QUALITY_MODE", "true").lower() == "true"
    server_url: str = os.getenv("SERVER_URL", "http://localhost:8000")
    worker_secret: str = os.getenv("WORKER_WEBHOOK_SECRET", "workersecret")


settings = Settings()
