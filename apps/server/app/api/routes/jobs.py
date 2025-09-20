from __future__ import annotations

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...core.deps import get_current_user, get_db
from ...models import Artifact, Job, Upload, User
from ...schemas.jobs import JobCreateRequest, JobResponse
from ...services.queue import enqueue_job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    payload: JobCreateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> JobResponse:
    upload = db.get(Upload, payload.upload_id)
    if not upload or upload.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Upload not found")
    job_id = str(uuid.uuid4())
    job = Job(
        id=job_id,
        owner_id=user.id,
        upload_id=upload.id,
        status="queued",
        progress=0,
        params_json={"quality_hint": payload.quality_hint},
    )
    db.add(job)
    db.commit()
    enqueue_job(job_id, {"upload_id": upload.id, "video_key": upload.s3_key})
    return JobResponse(id=job_id, status="queued", progress=0, artifacts=None)


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> JobResponse:
    job = db.get(Job, job_id)
    if not job or job.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    artifacts = (
        db.scalars(select(Artifact).where(Artifact.job_id == job.id, Artifact.deleted_at.is_(None))).all()
    )
    artifact_payload = None
    if artifacts:
        artifact = artifacts[0]
        artifact_payload = {
            "glb": artifact.glb_key,
            "usdz": artifact.usdz_key,
            "preview": artifact.preview_key,
            "meta": artifact.meta_json,
        }
    return JobResponse(
        id=job.id,
        status=job.status,
        progress=job.progress,
        artifacts=artifact_payload,
        error=job.params_json.get("error"),
        started_at=job.started_at,
        finished_at=job.finished_at,
    )
