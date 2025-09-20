from datetime import datetime

from pydantic import BaseModel

from ..schemas.auth import UserResponse


class PostCreateRequest(BaseModel):
    artifact_id: str
    caption: str
    tags: list[str] = []
    visibility: str = "public"


class PostResponse(BaseModel):
    id: str
    owner: UserResponse
    artifact_id: str
    caption: str
    tags: list[str]
    visibility: str
    created_at: datetime
    likes: int
    comments: int
    preview_url: str | None
    model_url: str | None

    class Config:
        from_attributes = True


class CommentCreateRequest(BaseModel):
    body: str


class CommentResponse(BaseModel):
    id: str
    body: str
    user: UserResponse
    created_at: datetime

    class Config:
        from_attributes = True
