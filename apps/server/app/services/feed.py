from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models import Artifact, Comment, Like, Post, User
from ..schemas.feed import FeedArtifact, FeedPost
from .storage import storage_client


def get_feed(session: Session, viewer_id: str | None = None) -> list[FeedPost]:
    posts = session.scalars(
        select(Post)
        .where(Post.deleted_at.is_(None), Post.visibility == "public")
        .order_by(Post.created_at.desc())
        .limit(50)
    ).all()

    feed: list[FeedPost] = []
    for post in posts:
        artifact: Artifact = post.artifact
        previewUrl = storage_client.presigned_url("artifacts", artifact.preview_key)
        glbUrl = storage_client.presigned_url("artifacts", artifact.glb_key)
        usdzUrl = storage_client.presigned_url("artifacts", artifact.usdz_key)
        likes = session.scalar(select(func.count(Like.id)).where(Like.post_id == post.id)) or 0
        comments = session.scalar(select(func.count(Comment.id)).where(Comment.post_id == post.id)) or 0
        hasLiked = False
        if viewer_id:
            hasLiked = (
                session.scalar(
                    select(Like).where(Like.post_id == post.id, Like.user_id == viewer_id)
                )
                is not None
            )
        feed.append(
            FeedPost(
                id=post.id,
                ownerId=post.owner_id,
                ownerName=post.owner.email,
                caption=post.caption,
                tags=post.tags,
                visibility=post.visibility,
                createdAt=post.created_at,
                artifact=FeedArtifact(
                    glbUrl=glbUrl,
                    usdzUrl=usdzUrl,
                    previewUrl=previewUrl,
                    quality=artifact.meta_json.get("quality", {}),
                ),
                likes=likes,
                comments=comments,
                hasLiked=hasLiked,
            )
        )
    return feed
