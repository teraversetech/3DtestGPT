from __future__ import annotations

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from .api.routes import auth, feed, jobs, posts, uploads, webhooks
from .core.config import get_settings
from .core.logging import setup_logging

settings = get_settings()
request_counter = Counter("fashion3d_requests_total", "Total HTTP requests", ["method", "path"])
request_histogram = Histogram("fashion3d_request_duration_seconds", "Request latency", ["method", "path"])


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title="Fashion3D API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(uploads.router)
    app.include_router(jobs.router)
    app.include_router(feed.router)
    app.include_router(posts.router)
    app.include_router(webhooks.router)

    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):  # type: ignore[override]
        path = request.url.path
        method = request.method
        with request_histogram.labels(method=method, path=path).time():
            response = await call_next(request)
        request_counter.labels(method=method, path=path).inc()
        return response

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/metrics", response_class=PlainTextResponse)
    async def metrics() -> PlainTextResponse:
        return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    return app


app = create_app()
