from datetime import datetime

from pydantic import BaseModel


class FeedArtifact(BaseModel):
    glbUrl: str
    usdzUrl: str
    previewUrl: str
    quality: dict


class FeedPost(BaseModel):
    id: str
    ownerId: str
    ownerName: str
    caption: str
    tags: list[str]
    visibility: str
    createdAt: datetime
    artifact: FeedArtifact
    likes: int
    comments: int
    hasLiked: bool = False
