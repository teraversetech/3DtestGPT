import os
import pathlib
import uuid

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///" + str(pathlib.Path("test.db").resolve()))
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("MINIO_ENDPOINT", "http://localhost:9000")
os.environ.setdefault("MINIO_ACCESS_KEY", "minioadmin")
os.environ.setdefault("MINIO_SECRET_KEY", "minioadmin")
os.environ.setdefault("MINIO_BUCKET_RAW", "raw-videos")
os.environ.setdefault("MINIO_BUCKET_ARTIFACTS", "artifacts")
os.environ.setdefault("JWT_SECRET", "testsecret")

from app.core.database import Base, engine, SessionLocal
from app.main import create_app


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    SessionLocal().close()


@pytest.fixture()
def client() -> TestClient:
    app = create_app()
    return TestClient(app)


@pytest.fixture()
def auth_token(client: TestClient) -> str:
    email = f"test-{uuid.uuid4()}@example.com"
    client.post("/auth/signup", json={"email": email, "password": "password"})
    response = client.post("/auth/login", json={"email": email, "password": "password"})
    return response.json()["access_token"]
