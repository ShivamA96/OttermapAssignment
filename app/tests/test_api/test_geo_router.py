import pytest
from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)


@pytest.fixture
def create_test_shops():
    user_data = {
        "name": "Geo Tester",
        "email": "geo_tester@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    token = response.json()["jwt_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    shop_locations = [
        {"name": "Shop 1", "business_type": "Retail",
            "latitude": 37.7749, "longitude": -122.4194},
        {"name": "Shop 2", "business_type": "Service",
            "latitude": 37.7850, "longitude": -122.4294},
        {"name": "Shop 3", "business_type": "Food",
            "latitude": 37.7650, "longitude": -122.4094},
    ]

    for shop_data in shop_locations:
        client.post("/api/v1/shops", json=shop_data, headers=auth_headers)


def test_search_nearby_shops(create_test_shops):
    search_data = {
        "lattitude": 37.7749,
        "longitude": -122.4194,
        "radius": 10.0,
        "limit": 5
    }
    response = client.post("/api/v1/search", json=search_data)
    assert response.status_code == 200
    shops = response.json()
    assert len(shops) > 0
    assert all("id" in shop for shop in shops)
    assert all("distance" in shop for shop in shops)


def test_search_no_shops_nearby():
    search_data = {
        "lattitude": 0.0,  # Middle of nowhere
        "longitude": 0.0,
        "radius": 1.0,
        "limit": 10
    }
    response = client.post("/api/v1/search", json=search_data)
    assert response.status_code == 404
