from __future__ import annotations

import json
from typing import Any

import rq
from redis import Redis

from ..core.config import get_settings

settings = get_settings()
redis_conn = Redis.from_url(settings.redis_url)
queue = rq.Queue("fashion3d", connection=redis_conn, default_timeout=60 * 60)


def enqueue_job(job_id: str, payload: dict[str, Any]) -> str:
    return queue.enqueue("fashion3d_worker.jobs.process_job", job_id, payload, job_id=job_id).id


def mark_job_progress(job_id: str, progress: int) -> None:
    meta_key = f"job:{job_id}:meta"
    redis_conn.hset(meta_key, "progress", progress)


def publish_job_status(job_id: str, status: str, data: dict[str, Any] | None = None) -> None:
    message = {"job_id": job_id, "status": status, "data": data or {}}
    redis_conn.publish("fashion3d:jobs", json.dumps(message))
