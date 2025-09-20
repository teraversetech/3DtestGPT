from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ...core.deps import get_current_user, get_db
from ...models import Artifact, Comment, Like, Post, User
from ...schemas.posts import CommentCreateRequest, CommentResponse, PostCreateRequest, PostResponse
from ...services.storage import storage_client

router = APIRouter(prefix="/posts", tags=["posts"])


def _serialize_post(post: Post, db: Session) -> PostResponse:
    likes = db.scalar(select(func.count(Like.id)).where(Like.post_id == post.id)) or 0
    comments_count = db.scalar(select(func.count(Comment.id)).where(Comment.post_id == post.id)) or 0
    artifact = post.artifact
    return PostResponse(
        id=post.id,
        owner=post.owner,
        artifact_id=artifact.id,
        caption=post.caption,
        tags=post.tags,
        visibility=post.visibility,
        created_at=post.created_at,
        likes=likes,
        comments=comments_count,
        preview_url=storage_client.presigned_url("artifacts", artifact.preview_key),
        model_url=storage_client.presigned_url("artifacts", artifact.glb_key),
    )


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    payload: PostCreateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> PostResponse:
    artifact = db.get(Artifact, payload.artifact_id)
    if not artifact or artifact.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Artifact not found")
    post = Post(
        id=str(uuid.uuid4()),
        owner_id=user.id,
        artifact_id=artifact.id,
        caption=payload.caption,
        tags=payload.tags,
        visibility=payload.visibility,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return _serialize_post(post, db)


@router.post("/{post_id}/like", status_code=status.HTTP_200_OK)
def like_post(
    post_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict[str, bool]:
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    existing = db.scalar(select(Like).where(Like.post_id == post_id, Like.user_id == user.id))
    if existing:
        return {"liked": True}
    like = Like(id=str(uuid.uuid4()), post_id=post_id, user_id=user.id)
    db.add(like)
    db.commit()
    return {"liked": True}


@router.post("/{post_id}/comment", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def comment_post(
    post_id: str,
    payload: CommentCreateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> CommentResponse:
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = Comment(id=str(uuid.uuid4()), post_id=post_id, user_id=user.id, body=payload.body)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return CommentResponse(id=comment.id, body=comment.body, user=user, created_at=comment.created_at)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> None:
    post = db.get(Post, post_id)
    if not post or post.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Post not found")
    post.deleted_at = post.deleted_at or post.created_at
    db.add(post)
    db.commit()


@router.delete("/artifacts/{artifact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_artifact(
    artifact_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:
    artifact = db.get(Artifact, artifact_id)
    if not artifact or artifact.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Artifact not found")
    artifact.deleted_at = artifact.deleted_at or artifact.created_at
    db.add(artifact)
    db.commit()
