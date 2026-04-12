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


def test_customer_login_and_protected_route() -> None:
    client = TestClient(app)

    r = client.post(
        "/customers/",
        json={
            "customer_name": "Auth User",
            "customer_email": f"auth{__import__('time').time_ns()}@example.com",
            "phone_number": "0123456789",
            "address": "Auth Address",
            "password": "123456",
        },
    )
    assert r.status_code == 201
    customer = r.json()

    r = client.post(
        "/customers/login",
        json={"email_or_phone": customer["customer_email"], "password": "123456"},
    )
    assert r.status_code == 200
    token = r.json()["access_token"]

    r = client.get(
        f"/customers/{customer['customer_id']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
