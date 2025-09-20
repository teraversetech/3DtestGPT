from datetime import datetime

from pydantic import BaseModel


class UploadInitRequest(BaseModel):
    filename: str
    filesize: int
    content_type: str
    face_blur: bool = False


class UploadInitResponse(BaseModel):
    upload_id: str
    upload_url: str
    chunk_size: int


class UploadPartRequest(BaseModel):
    part_number: int
    content_length: int


class UploadCompleteRequest(BaseModel):
    parts: list[int]


class UploadResponse(BaseModel):
    id: str
    s3_key: str
    size: int
    parts: int
    created_at: datetime

    class Config:
        from_attributes = True
