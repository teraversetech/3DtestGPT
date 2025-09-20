from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ..models import User
from .config import get_settings
from .database import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
settings = get_settings()


def get_db() -> Session:
    with get_session() as session:
        yield session


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as exc:  # pragma: no cover - direct bubble up
        raise credentials_exception from exc
    user = db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    authorization = request.headers.get("Authorization")
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        return None
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if not user_id:
            return None
    except JWTError:
        return None
    return db.get(User, user_id)
