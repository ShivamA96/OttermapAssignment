import pytest
from fastapi.testclient import TestClient
from app.src.main import app
from app.src.models.user_model import User
from app.src.models.shop_model import Shop
client = TestClient(app)


@pytest.fixture
def auth_headers():
    # Create a test user and get token
    user_data = {
        "name": "Test User",
        "email": "test_router@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    token = response.json()["jwt_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_user(auth_headers):
    user_id = client.get("/api/v1/users/me", headers=auth_headers).json()["id"]
    response = client.get(f"/api/v1/users/{user_id}", headers=auth_headers)
    assert response.status_code == 200
    assert "id" in response.json()


def test_update_user(auth_headers):
    update_data = {
        "name": "Updated Name"
    }
    response = client.put(
        "/api/v1/users/", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


def test_delete_user(auth_headers):
    response = client.delete("/api/v1/users/", headers=auth_headers)
    assert response.status_code == 204
