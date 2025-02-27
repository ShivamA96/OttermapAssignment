import pytest
from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)


def test_register():
    user_data = {
        "name": "Test Register",
        "email": "test_register@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    assert "jwt_token" in response.json()
    assert "user_id" in response.json()


def test_login():
    user_data = {
        "name": "Test Login",
        "email": "test_login@example.com",
        "password": "password123"
    }
    client.post("/api/v1/auth/register", json=user_data)

    login_data = {
        "email": "test_login@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    assert "jwt_token" in response.json()
    assert "user_id" in response.json()


def test_login_invalid():
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401
