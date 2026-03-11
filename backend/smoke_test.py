import time
from typing import Any

from fastapi.testclient import TestClient

from app.main import app

##
def _json(r) -> Any:
    assert r.status_code < 500, f"{r.status_code} {r.text}"
    if r.status_code >= 400:
        raise RuntimeError(f"{r.status_code} {r.text}")
    if r.status_code == 204:
        return None
    return r.json()


def run() -> None:
    client = TestClient(app)

    root = _json(client.get("/"))
    assert isinstance(root, dict) and "message" in root

    test_db = _json(client.get("/test-db"))
    assert test_db.get("result") == 1

    cat = _json(client.post("/categories/", json={"category_name": f"SmokeCat {int(time.time())}"}))
    category_id = cat["category_id"]

    pm = _json(client.post("/payment-methods/", json={"mode_name": "COD"}))
    payment_method_id = pm["payment_method_id"]

    cust = _json(
        client.post(
            "/customers/",
            json={
                "customer_name": "Smoke User",
                "customer_email": f"smoke{int(time.time())}@example.com",
                "phone_number": "0123456789",
                "address": "Smoke Address",
                "password": "123456",
            },
        )
    )
    customer_id = cust["customer_id"]

    token_resp = _json(
        client.post(
            "/customers/login",
            json={"email_or_phone": cust["customer_email"], "password": "123456"},
        )
    )
    customer_token = token_resp["access_token"]
    customer_headers = {"Authorization": f"Bearer {customer_token}"}

    prod = _json(
        client.post(
            "/products/",
            json={
                "product_name": "Smoke Product",
                "unit_price": 10,
                "category_id": category_id,
                "stock_quantity": 3,
            },
        )
    )
    product_id = prod["product_id"]

    order = _json(
        client.post(
            "/orders/",
            json={
                "customer_id": customer_id,
                "payment_method_id": payment_method_id,
                "items": [{"product_id": product_id, "quantity": 1}],
            },
            headers=customer_headers,
        )
    )
    order_id = order["order_id"]

    app_prod = _json(client.get(f"/products/{product_id}"))
    assert app_prod["product_id"] == product_id
    assert app_prod["category_id"] == category_id

    my_orders = _json(client.get("/orders/?skip=0&limit=10", headers=customer_headers))
    assert isinstance(my_orders, list)

    token_resp = _json(
        client.post(
            "/admin/login",
            data={"username": "admin", "password": "admin123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    )
    token = token_resp["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    admin_prod = _json(client.get(f"/admin/products/{product_id}", headers=headers))
    assert admin_prod["product_id"] == product_id

    patched = _json(
        client.patch(
            f"/admin/orders/{order_id}/status",
            json={"status": "Shipped"},
            headers=headers,
        )
    )
    assert patched["order_id"] == order_id

    print("SMOKE TEST: OK")


if __name__ == "__main__":
    run()
