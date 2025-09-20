"""Download sample capture for Fashion3D demo."""

from __future__ import annotations

import argparse
from pathlib import Path

import requests

SAMPLE_URL = "https://huggingface.co/datasets/hf-internal-testing/fixtures/resolve/main/one-second-video.mp4"


def download(destination: Path) -> None:
    response = requests.get(SAMPLE_URL, timeout=60)
    response.raise_for_status()
    destination.write_bytes(response.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("sample.mp4"))
    args = parser.parse_args()
    download(args.output)
    print(f"Downloaded sample video to {args.output}")
