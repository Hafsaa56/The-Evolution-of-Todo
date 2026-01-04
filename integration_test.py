"""
Basic integration test to verify frontend-backend communication.
This test checks that API endpoints are accessible and properly secured.
"""
import requests
import pytest
import subprocess
import time
import os

# Configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

def test_backend_health():
    """Test that the backend is running and accessible."""
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
        print("✓ Backend health check passed")
    except requests.exceptions.ConnectionError:
        print("✗ Backend is not running or not accessible")
        raise

def test_api_documentation():
    """Test that API documentation is available."""
    try:
        response = requests.get(f"{BACKEND_URL}/docs")
        assert response.status_code == 200
        print("✓ API documentation is accessible")
    except requests.exceptions.ConnectionError:
        print("✗ API documentation is not accessible")
        raise

def test_auth_endpoints_exist():
    """Test that auth endpoints exist (they should return 400/401 for missing data, not 404)."""
    # Test register endpoint
    response = requests.post(f"{BACKEND_URL}/api/auth/register", json={})
    assert response.status_code in [400, 422]  # Validation error expected, not 404

    # Test login endpoint
    response = requests.post(f"{BACKEND_URL}/api/auth/login", json={})
    assert response.status_code in [400, 422]  # Validation error expected, not 404

    print("✓ Auth endpoints exist")

def test_protected_endpoints_require_auth():
    """Test that protected endpoints require authentication."""
    response = requests.get(f"{BACKEND_URL}/api/tasks/")
    assert response.status_code == 401  # Unauthorized

    print("✓ Protected endpoints require authentication")

def run_integration_tests():
    """Run all integration tests."""
    print("Running integration tests...")

    # Run tests
    test_backend_health()
    test_api_documentation()
    test_auth_endpoints_exist()
    test_protected_endpoints_require_auth()

    print("\n✓ All integration tests passed!")

if __name__ == "__main__":
    run_integration_tests()