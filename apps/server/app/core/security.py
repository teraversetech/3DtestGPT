from datetime import datetime, timedelta
from typing import Any, Dict

from jose import jwt
from passlib.context import CryptContext

from .config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.jwt_expire_minutes)
    expire = datetime.utcnow() + expires_delta
    to_encode: Dict[str, Any] = {"exp": expire, "sub": subject}
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
