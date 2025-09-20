#!/bin/bash
set -euo pipefail

poetry install --no-interaction --no-ansi
poetry run python -m fashion3d_worker.cli worker
