import pytest
from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)


@pytest.fixture
def auth_headers():
    user_data = {
        "name": "Shop Owner",
        "email": "shop_owner@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    token = response.json()["jwt_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def shop_id(auth_headers):
    shop_data = {
        "name": "Test Shop",
        "business_type": "Retail",
        "latitude": 37.7749,
        "longitude": -122.4194
    }
    response = client.post(
        "/api/v1/shops", json=shop_data, headers=auth_headers)
    return response.json()["id"]


def test_create_shop(auth_headers):
    shop_data = {
        "name": "New Test Shop",
        "business_type": "Service",
        "latitude": 37.7750,
        "longitude": -122.4195
    }
    response = client.post(
        "/api/v1/shops", json=shop_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == "New Test Shop"


def test_get_shop(auth_headers, shop_id):
    response = client.get(f"/api/v1/shops/{shop_id}")
    assert response.status_code == 200
    assert response.json()["id"] == shop_id


def test_get_user_shops(auth_headers, shop_id):
    response = client.get("/api/v1/shops", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert any(shop["id"] == shop_id for shop in response.json())


def test_update_shop(auth_headers, shop_id):
    update_data = {
        "name": "Updated Shop Name"
    }
    response = client.put(
        f"/api/v1/shops/{shop_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Shop Name"


def test_delete_shop(auth_headers, shop_id):
    response = client.delete(f"/api/v1/shops/{shop_id}", headers=auth_headers)
    assert response.status_code == 200
    assert "detail" in response.json()
