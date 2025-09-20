from pathlib import Path

import cv2
import numpy as np

from fashion3d_worker.pipeline import run_pipeline


def test_pipeline_generates_artifacts(tmp_path: Path) -> None:
    video_path = tmp_path / "demo.mp4"
    height, width = 32, 32
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(video_path), fourcc, 5, (width, height))
    for i in range(5):
        frame = np.full((height, width, 3), i * 10, dtype=np.uint8)
        writer.write(frame)
    writer.release()

    outputs = run_pipeline("test-job", video_path)
    assert outputs["glb"].exists()
    assert outputs["preview"].exists()
    assert outputs["quality"].exists()
