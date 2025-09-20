from __future__ import annotations

import json
import uuid

from sqlalchemy import select

from ..core.database import get_session
from ..core.security import get_password_hash
from ..models import Artifact, Job, Post, Upload, User


DUMMY_USER_EMAIL = "demo@fashion3d.dev"


def seed() -> None:
    with get_session() as session:
        user = session.scalar(select(User).where(User.email == DUMMY_USER_EMAIL))
        if not user:
            user = User(
                id=str(uuid.uuid4()),
                email=DUMMY_USER_EMAIL,
                password_hash=get_password_hash("password"),
                plan="pro",
            )
            session.add(user)

        upload = Upload(
            id=str(uuid.uuid4()),
            owner_id=user.id,
            s3_key="demo/source.mp4",
            size=10,
            parts=1,
        )
        job = Job(
            id=str(uuid.uuid4()),
            owner_id=user.id,
            upload_id=upload.id,
            status="succeeded",
            progress=100,
        )
        artifact = Artifact(
            id=str(uuid.uuid4()),
            job_id=job.id,
            owner_id=user.id,
            glb_key="artifacts/demo/model.glb",
            usdz_key="artifacts/demo/model.usdz",
            preview_key="artifacts/demo/preview.jpg",
            meta_json={"quality": {"psnr": 25.4, "ssim": 0.88, "completeness": 0.92}},
        )
        post = Post(
            id=str(uuid.uuid4()),
            owner_id=user.id,
            artifact_id=artifact.id,
            caption="Runway look - neon jacket",
            tags=["runway", "neon", "ss24"],
            visibility="public",
        )
        for entity in [upload, job, artifact, post]:
            session.merge(entity)
        session.commit()
        print("Seeded demo data")


if __name__ == "__main__":
    seed()
