from __future__ import annotations

import io
import os
from pathlib import Path
from typing import BinaryIO

from minio import Minio

from ..core.config import get_settings

settings = get_settings()


class StorageClient:
    def __init__(self) -> None:
        self._fallback_dir = Path(os.getenv("STORAGE_FALLBACK_DIR", "./artifacts"))
        self._fallback_dir.mkdir(parents=True, exist_ok=True)
        endpoint = settings.minio_endpoint.replace("http://", "").replace("https://", "")
        secure = settings.minio_endpoint.startswith("https://")
        self.client = Minio(
            endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=secure,
        )
        for bucket in [settings.minio_bucket_raw, settings.minio_bucket_artifacts]:
            try:
                if not self.client.bucket_exists(bucket):
                    self.client.make_bucket(bucket)
            except Exception:
                # Offline fallback mode
                pass

    def upload_raw_part(self, upload_id: str, part_number: int, data: bytes) -> str:
        key = f"{upload_id}/parts/{part_number:05d}.mp4"
        try:
            self.client.put_object(
                settings.minio_bucket_raw,
                key,
                io.BytesIO(data),
                length=len(data),
                content_type="video/mp4",
            )
        except Exception:
            part_path = self._fallback_dir / key
            part_path.parent.mkdir(parents=True, exist_ok=True)
            part_path.write_bytes(data)
        return key

    def compose_raw_video(self, upload_id: str, total_parts: int) -> str:
        composed_key = f"{upload_id}/source.mp4"
        # TODO: Use MinIO compose API for server-side concatenation
        try:
            data = bytearray()
            for part_number in range(1, total_parts + 1):
                part_key = f"{upload_id}/parts/{part_number:05d}.mp4"
                response = self.client.get_object(settings.minio_bucket_raw, part_key)
                data.extend(response.read())
            self.client.put_object(
                settings.minio_bucket_raw,
                composed_key,
                io.BytesIO(bytes(data)),
                length=len(data),
                content_type="video/mp4",
            )
        except Exception:
            composed_path = self._fallback_dir / composed_key
            composed_path.parent.mkdir(parents=True, exist_ok=True)
            with composed_path.open("wb") as f:
                for part_number in range(1, total_parts + 1):
                    part_path = self._fallback_dir / f"{upload_id}/parts/{part_number:05d}.mp4"
                    if part_path.exists():
                        f.write(part_path.read_bytes())
        return composed_key

    def upload_artifact_file(self, job_id: str, filename: str, stream: BinaryIO, content_type: str) -> str:
        key = f"artifacts/{job_id}/{filename}"
        data = stream.read()
        try:
            self.client.put_object(
                settings.minio_bucket_artifacts,
                key,
                io.BytesIO(data),
                length=len(data),
                content_type=content_type,
            )
        except Exception:
            artifact_path = self._fallback_dir / key
            artifact_path.parent.mkdir(parents=True, exist_ok=True)
            artifact_path.write_bytes(data)
        return key

    def presigned_url(self, bucket: str, key: str, expiry: int = 3600) -> str:
        try:
            return self.client.presigned_get_object(bucket, key, expires=expiry)
        except Exception:
            return str((self._fallback_dir / key).resolve())


storage_client = StorageClient()
