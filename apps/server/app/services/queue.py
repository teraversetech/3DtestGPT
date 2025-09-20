from __future__ import annotations

import json
from typing import Any

import rq
from redis import Redis
from redis.exceptions import RedisError

from ..core.config import get_settings

settings = get_settings()

_fallback_jobs: dict[str, dict[str, Any]] = {}
_fallback_meta: dict[str, dict[str, Any]] = {}
_fallback_events: list[dict[str, Any]] = []

try:
    redis_conn = Redis.from_url(
        settings.redis_url, socket_connect_timeout=0.5, socket_timeout=0.5
    )
    redis_conn.ping()
    queue = rq.Queue("fashion3d", connection=redis_conn, default_timeout=60 * 60)
except Exception:
    redis_conn = None
    queue = None


def enqueue_job(job_id: str, payload: dict[str, Any]) -> str:
    if queue is not None:
        try:
            return queue.enqueue(
                "fashion3d_worker.jobs.process_job", job_id, payload, job_id=job_id
            ).id
        except RedisError:
            pass
    _fallback_jobs[job_id] = payload
    return job_id


def mark_job_progress(job_id: str, progress: int) -> None:
    if redis_conn is not None:
        try:
            meta_key = f"job:{job_id}:meta"
            redis_conn.hset(meta_key, "progress", progress)
            return
        except RedisError:
            pass
    meta = _fallback_meta.setdefault(job_id, {})
    meta["progress"] = progress


def publish_job_status(job_id: str, status: str, data: dict[str, Any] | None = None) -> None:
    message = {"job_id": job_id, "status": status, "data": data or {}}
    if redis_conn is not None:
        try:
            redis_conn.publish("fashion3d:jobs", json.dumps(message))
            return
        except RedisError:
            pass
    _fallback_events.append(message)
