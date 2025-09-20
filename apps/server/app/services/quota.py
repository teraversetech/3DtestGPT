from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.config import get_settings
from ..models import ScanQuota, User

settings = get_settings()


def _month_key() -> str:
    return datetime.utcnow().strftime("%Y-%m")


def ensure_quota(session: Session, user: User) -> None:
    month = _month_key()
    quota = session.scalar(
        select(ScanQuota).where(ScanQuota.user_id == user.id, ScanQuota.month == month)
    )
    if quota is None:
        quota = ScanQuota(user_id=user.id, month=month, used_scans=0, plan=user.plan)
        session.add(quota)
        session.flush()
    limit = settings.rate_free_scans if user.plan == "free" else 9999
    if quota.used_scans >= limit:
        raise PermissionError("Free tier limit exceeded")


def increment_quota(session: Session, user: User) -> None:
    month = _month_key()
    quota = session.scalar(
        select(ScanQuota).where(ScanQuota.user_id == user.id, ScanQuota.month == month)
    )
    if quota is None:
        quota = ScanQuota(user_id=user.id, month=month, used_scans=0, plan=user.plan)
        session.add(quota)
        session.flush()
    quota.used_scans += 1
    session.add(quota)
