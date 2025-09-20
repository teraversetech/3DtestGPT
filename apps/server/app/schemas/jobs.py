from datetime import datetime

from pydantic import BaseModel, HttpUrl


class JobCreateRequest(BaseModel):
    upload_id: str
    video_url: HttpUrl | None = None
    quality_hint: str | None = None


class JobResponse(BaseModel):
    id: str
    status: str
    progress: int
    artifacts: dict | None
    error: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None

    class Config:
        from_attributes = True
