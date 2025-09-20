from __future__ import annotations

import hmac
import json
from hashlib import sha256
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from ...core.config import get_settings
from ...core.deps import get_db
from ...models import Artifact, Job

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
settings = get_settings()


@router.post("/stripe", status_code=status.HTTP_202_ACCEPTED)
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)) -> dict[str, str]:
    # TODO: integrate real Stripe signature verification
    payload = await request.body()
    return {"status": "received", "raw": payload.decode()}


@router.post("/worker", status_code=status.HTTP_202_ACCEPTED)
async def worker_webhook(
    request: Request,
    x_worker_signature: str = Header(""),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    body = await request.body()
    expected = hmac.new(settings.worker_webhook_secret.encode(), body, sha256).hexdigest()
    if not hmac.compare_digest(expected, x_worker_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    payload = json.loads(body)
    job = db.get(Job, payload["job_id"])
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.status = payload.get("status", job.status)
    job.progress = payload.get("progress", job.progress)
    if payload.get("status") == "processing":
        job.started_at = job.started_at or job.created_at
    if payload.get("status") == "succeeded":
        job.finished_at = job.finished_at or job.created_at
    if payload.get("status") == "failed":
        job.finished_at = job.finished_at or job.created_at
        job.params_json["error"] = payload.get("error")
    artifacts = payload.get("artifacts", [])
    for artifact_payload in artifacts:
        artifact = Artifact(
            id=artifact_payload["id"],
            job_id=job.id,
            owner_id=job.owner_id,
            glb_key=artifact_payload["glb_key"],
            usdz_key=artifact_payload["usdz_key"],
            preview_key=artifact_payload["preview_key"],
            meta_json=artifact_payload.get("meta", {}),
        )
        db.merge(artifact)
    db.add(job)
    db.commit()
    return {"ok": True}
