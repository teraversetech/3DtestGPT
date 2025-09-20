from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

import requests
from minio import Minio

from .config import settings
from .logging import logger, setup_logging
from .pipeline import run_pipeline


def _client() -> Minio:
    endpoint = settings.minio_endpoint.replace("http://", "").replace("https://", "")
    secure = settings.minio_endpoint.startswith("https://")
    client = Minio(endpoint, access_key=settings.minio_access_key, secret_key=settings.minio_secret_key, secure=secure)
    for bucket in [settings.minio_bucket_raw, settings.minio_bucket_artifacts]:
        try:
            if not client.bucket_exists(bucket):
                client.make_bucket(bucket)
        except Exception:
            pass
    return client


def _download_video(client: Minio, video_key: str, destination: Path) -> Path:
    response = client.get_object(settings.minio_bucket_raw, video_key)
    destination.write_bytes(response.read())
    return destination


def _upload_artifacts(client: Minio, job_id: str, artifacts: dict[str, Path]) -> None:
    for name, path in artifacts.items():
        object_name = f"artifacts/{job_id}/{path.name}"
        client.fput_object(settings.minio_bucket_artifacts, object_name, str(path))


def _notify_server(job_id: str, status: str, payload: dict[str, Any]) -> None:
    body = json.dumps({"job_id": job_id, "status": status, **payload}).encode()
    signature = hmac.new(settings.worker_secret.encode(), body, hashlib.sha256).hexdigest()
    response = requests.post(
        f"{settings.server_url}/webhooks/worker",
        headers={"X-Worker-Signature": signature, "Content-Type": "application/json"},
        data=body,
        timeout=30,
    )
    response.raise_for_status()


def process_job(job_id: str, payload: dict[str, Any]) -> None:
    setup_logging()
    logger.info("job.received", job_id=job_id, payload=payload)
    client = _client()
    tmp_video = Path(f"/tmp/{job_id}.mp4")
    video_key = payload.get("video_key")
    if not video_key:
        raise RuntimeError("Missing video key")
    _notify_server(job_id, "processing", {"progress": 10})
    _download_video(client, video_key, tmp_video)
    outputs = run_pipeline(job_id, tmp_video)
    _upload_artifacts(client, job_id, outputs)
    quality = json.loads(outputs["quality"].read_text())
    artifact_payload = {
        "id": f"{job_id}-primary",
        "glb_key": f"artifacts/{job_id}/model.glb",
        "usdz_key": f"artifacts/{job_id}/model.usdz",
        "preview_key": f"artifacts/{job_id}/preview.jpg",
        "meta": {"quality": quality},
    }
    _notify_server(job_id, "succeeded", {"progress": 100, "artifacts": [artifact_payload]})
    logger.info("job.completed", job_id=job_id)
