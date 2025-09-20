from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.deps import get_db, get_optional_user
from ...schemas.feed import FeedPost
from ...services.feed import get_feed

router = APIRouter(tags=["feed"])


@router.get("/feed", response_model=list[FeedPost])
def feed(db: Session = Depends(get_db), user=Depends(get_optional_user)) -> list[FeedPost]:
    viewer_id = user.id if user else None
    return get_feed(db, viewer_id)
