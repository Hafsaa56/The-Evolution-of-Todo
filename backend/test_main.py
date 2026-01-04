import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo API is running!"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_auth_routes_exist():
    # Test that auth routes exist (they will fail due to missing data, but should return 422 or 400, not 404)
    response = client.post("/auth/register")
    assert response.status_code in [422, 400]  # Validation error is expected

    response = client.post("/auth/login")
    assert response.status_code in [422, 400]  # Validation error is expected

def test_tasks_routes_exist():
    # Test that tasks routes exist (they will fail due to missing auth, but should return 401, not 404)
    response = client.get("/tasks")
    assert response.status_code == 401  # Unauthorized is expected without auth header

    response = client.post("/tasks")
    assert response.status_code == 401  # Unauthorized is expected without auth header