from fastapi.testclient import TestClient

CHUNK = b"0" * (1024 * 1024)


def _perform_upload(client: TestClient, token: str) -> None:
    init = client.post(
        "/uploads/init",
        json={"filename": "demo.mp4", "filesize": len(CHUNK), "content_type": "video/mp4"},
        headers={"Authorization": f"Bearer {token}"},
    )
    upload_id = init.json()["upload_id"]
    client.put(
        f"/uploads/{upload_id}/part",
        params={"part_number": 1},
        files={"file": ("chunk.mp4", CHUNK, "video/mp4")},
        headers={"Authorization": f"Bearer {token}"},
    )
    complete = client.post(
        f"/uploads/{upload_id}/complete",
        json={"parts": [1]},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert complete.status_code == 200


def test_quota_enforced(client: TestClient, auth_token: str) -> None:
    for _ in range(3):
        _perform_upload(client, auth_token)
    response = client.post(
        "/uploads/init",
        json={"filename": "demo.mp4", "filesize": len(CHUNK), "content_type": "video/mp4"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 402
