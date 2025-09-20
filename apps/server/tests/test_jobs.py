from fastapi.testclient import TestClient

from tests.test_quota import CHUNK, _perform_upload


def test_create_job(client: TestClient, auth_token: str) -> None:
    _perform_upload(client, auth_token)
    uploads = client.get(
        "/uploads/init",  # intentionally hitting GET to ensure 405 for coverage
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert uploads.status_code == 405
    payload = client.post(
        "/uploads/init",
        json={"filename": "demo.mp4", "filesize": len(CHUNK), "content_type": "video/mp4"},
        headers={"Authorization": f"Bearer {auth_token}"},
    ).json()
    upload_id = payload["upload_id"]
    client.put(
        f"/uploads/{upload_id}/part",
        params={"part_number": 1},
        files={"file": ("chunk.mp4", CHUNK, "video/mp4")},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    client.post(
        f"/uploads/{upload_id}/complete",
        json={"parts": [1]},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    response = client.post(
        "/jobs",
        json={"upload_id": upload_id},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 201
    job_id = response.json()["id"]
    detail = client.get(f"/jobs/{job_id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert detail.status_code == 200
