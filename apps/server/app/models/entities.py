from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.database import Base
from .common import SoftDeleteMixin, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    plan: Mapped[str] = mapped_column(String(50), default="free")

    uploads: Mapped[list[Upload]] = relationship("Upload", back_populates="owner")
    jobs: Mapped[list[Job]] = relationship("Job", back_populates="owner")
    posts: Mapped[list[Post]] = relationship("Post", back_populates="owner")


class Upload(Base, TimestampMixin):
    __tablename__ = "uploads"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    s3_key: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[int] = mapped_column(default=0)
    parts: Mapped[int] = mapped_column(default=0)

    owner: Mapped[User] = relationship("User", back_populates="uploads")
    jobs: Mapped[list[Job]] = relationship("Job", back_populates="upload")


class Job(Base, TimestampMixin):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    upload_id: Mapped[str] = mapped_column(ForeignKey("uploads.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="queued")
    progress: Mapped[int] = mapped_column(default=0)
    params_json: Mapped[dict] = mapped_column(JSON, default=dict)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    owner: Mapped[User] = relationship("User", back_populates="jobs")
    upload: Mapped[Upload] = relationship("Upload", back_populates="jobs")
    artifacts: Mapped[list[Artifact]] = relationship("Artifact", back_populates="job")


class Artifact(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "artifacts"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    glb_key: Mapped[str] = mapped_column(String(255), nullable=False)
    usdz_key: Mapped[str] = mapped_column(String(255), nullable=False)
    preview_key: Mapped[str] = mapped_column(String(255), nullable=False)
    meta_json: Mapped[dict] = mapped_column(JSON, default=dict)

    job: Mapped[Job] = relationship("Job", back_populates="artifacts")
    owner: Mapped[User] = relationship("User")
    posts: Mapped[list[Post]] = relationship("Post", back_populates="artifact")


class Post(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    artifact_id: Mapped[str] = mapped_column(ForeignKey("artifacts.id"), nullable=False)
    caption: Mapped[str] = mapped_column(Text, default="")
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    visibility: Mapped[str] = mapped_column(String(20), default="public")

    owner: Mapped[User] = relationship("User", back_populates="posts")
    artifact: Mapped[Artifact] = relationship("Artifact", back_populates="posts")
    likes: Mapped[list[Like]] = relationship("Like", back_populates="post")
    comments: Mapped[list[Comment]] = relationship("Comment", back_populates="post")


class Like(Base, TimestampMixin):
    __tablename__ = "likes"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    post_id: Mapped[str] = mapped_column(ForeignKey("posts.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)

    post: Mapped[Post] = relationship("Post", back_populates="likes")
    user: Mapped[User] = relationship("User")


class Comment(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "comments"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    post_id: Mapped[str] = mapped_column(ForeignKey("posts.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    post: Mapped[Post] = relationship("Post", back_populates="comments")
    user: Mapped[User] = relationship("User")


class ScanQuota(Base):
    __tablename__ = "scan_quotas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    month: Mapped[str] = mapped_column(String(7), nullable=False)
    used_scans: Mapped[int] = mapped_column(default=0)
    plan: Mapped[str] = mapped_column(String(50), default="free")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()")

    user: Mapped[User] = relationship("User")

    __table_args__ = ({"sqlite_autoincrement": True},)
