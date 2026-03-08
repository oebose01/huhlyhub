from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_content():
    response = client.post(
        "/api/register-content",
        json={"content_hash": "testhash123", "user_id": "user123"},
    )
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_verify_existing():
    # Register
    client.post(
        "/api/register-content",
        json={"content_hash": "testhash456", "user_id": "user123"},
    )
    # Verify
    response = client.post("/api/verify-content", json={"content_hash": "testhash456"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["content_hash"] == "testhash456"


def test_verify_nonexistent():
    response = client.post("/api/verify-content", json={"content_hash": "nonexistent"})
    assert response.status_code == 200
    assert response.json()["success"] is False
