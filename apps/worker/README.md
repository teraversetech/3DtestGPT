# Fashion3D Worker

Python worker that consumes reconstruction jobs from Redis/RQ, retrieves the raw capture from MinIO, runs a CPU-friendly Gaussian-splat inspired pipeline, and writes GLB/USDZ artifacts back to object storage.

## Quick start

```bash
poetry install
poetry run pytest
poetry run python -m fashion3d_worker.cli worker
```

Environment variables live in `.env.example`. When running locally without MinIO the worker falls back to writing files under `/tmp/artifacts`.

## Pipeline overview

1. Download capture video and extract frames with OpenCV (auto brightness equalisation + TODO: face blur using MediaPipe).
2. Generate a lightweight point cloud proxy and export placeholder glTF/GLB + stub USDZ (replace with full USD stage in production).
3. Compute quality metrics (PSNR/SSIM heuristics) saved to `quality.json`.
4. Upload `preview.jpg`, `model.glb`, `model.usdz`, and `quality.json` to `artifacts/{job_id}/`.
5. Notify the API via signed webhook (`WORKER_WEBHOOK_SECRET`).

GPU mode can be enabled with `GPU_ENABLED=true` and swapping `_generate_dummy_point_cloud` with a real Gaussian Splatting implementation (see TODO markers in `pipeline.py`).

## Sample data

Grab a demo capture:

```bash
poetry run python scripts/download_sample.py --output sample.mp4
```

## Tests

```bash
poetry run pytest
```
