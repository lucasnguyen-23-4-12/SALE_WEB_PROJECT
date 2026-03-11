from fastapi.testclient import TestClient

from app.main import app


def test_smoke_root_and_admin_login() -> None:
    client = TestClient(app)

    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()

    r = client.get("/test-db")
    assert r.status_code == 200
    assert r.json().get("result") == 1

    r = client.post(
        "/admin/login",
        data={"username": "admin", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200
    assert r.json().get("token_type") == "bearer"
