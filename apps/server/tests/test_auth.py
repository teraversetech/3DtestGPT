from fastapi.testclient import TestClient


def test_signup_and_login(client: TestClient) -> None:
    payload = {"email": "user@example.com", "password": "secret"}
    response = client.post("/auth/signup", json=payload)
    assert response.status_code == 201
    login = client.post("/auth/login", json=payload)
    assert login.status_code == 200
    assert "access_token" in login.json()
