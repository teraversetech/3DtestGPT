from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from ...core.deps import get_current_user, get_db
from ...models import Upload, User
from ...schemas.uploads import (
    UploadCompleteRequest,
    UploadInitRequest,
    UploadInitResponse,
    UploadResponse,
)
from ...services import quota
from ...services.storage import storage_client

router = APIRouter(prefix="/uploads", tags=["uploads"])
CHUNK_SIZE = 10 * 1024 * 1024


@router.post("/init", response_model=UploadInitResponse)
def init_upload(
    payload: UploadInitRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UploadInitResponse:
    try:
        quota.ensure_quota(db, user)
    except PermissionError:
        raise HTTPException(status_code=402, detail="Monthly scan quota exceeded")
    upload_id = str(uuid.uuid4())
    upload = Upload(
        id=upload_id,
        owner_id=user.id,
        s3_key=f"{upload_id}/source.mp4",
        size=payload.filesize,
        parts=0,
    )
    db.add(upload)
    db.commit()
    return UploadInitResponse(upload_id=upload_id, upload_url=f"/uploads/{upload_id}/part", chunk_size=CHUNK_SIZE)


@router.put("/{upload_id}/part", response_model=UploadResponse)
def upload_part(
    upload_id: str,
    part_number: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UploadResponse:
    upload = db.get(Upload, upload_id)
    if not upload or upload.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Upload not found")
    data = file.file.read()
    if len(data) > CHUNK_SIZE + 1024 * 1024:
        raise HTTPException(status_code=400, detail="Chunk too large")
    storage_client.upload_raw_part(upload_id, part_number, data)
    upload.parts = max(upload.parts, part_number)
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return UploadResponse.model_validate(upload)


@router.post("/{upload_id}/complete", response_model=UploadResponse)
def complete_upload(
    upload_id: str,
    payload: UploadCompleteRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UploadResponse:
    upload = db.get(Upload, upload_id)
    if not upload or upload.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Upload not found")
    storage_client.compose_raw_video(upload_id, len(payload.parts))
    quota.increment_quota(db, user)
    db.refresh(upload)
    return UploadResponse.model_validate(upload)
