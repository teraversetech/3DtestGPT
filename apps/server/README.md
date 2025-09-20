# Fashion3D Server

FastAPI application providing authentication, upload orchestration, job management, feed APIs, and webhook handling for the Fashion3D platform.

## Getting started

```bash
poetry install
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```

Set environment variables via `.env` (see `.env.example`).

## Key features

- JWT authentication and free-tier quota enforcement.
- Chunked video uploads stored in MinIO (with filesystem fallback for local testing).
- Job queueing via Redis/RQ and webhook notifications from workers.
- REST feed, posts, likes, and comments endpoints backing both mobile and web clients.
- Prometheus metrics (`/metrics`) and structured logging with `structlog`.

## API cheatsheet

```bash
# Signup
curl -X POST http://localhost:8000/auth/signup \
  -H 'Content-Type: application/json' \
  -d '{"email":"demo@example.com","password":"secret"}'

# Login
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"demo@example.com","password":"secret"}' | jq -r '.access_token')

# Initiate upload
curl -s -X POST http://localhost:8000/uploads/init \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"filename":"look.mp4","filesize":1048576,"content_type":"video/mp4"}'

# Create job
curl -s -X POST http://localhost:8000/jobs \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"upload_id":"<upload-id>"}'

# Poll job
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/jobs/<job-id>
```

## Running tests

```bash
poetry run pytest
```

## Stripe webhook stub

`POST /webhooks/stripe` simply echoes the payload today. Replace with real signature verification when Stripe secrets are available. Worker webhooks are signed with `WORKER_WEBHOOK_SECRET`.

## Seeding demo content

```bash
poetry run python app/scripts/seed.py
```

This creates a pro demo user with a staged artifact so the feed renders immediately in development.
