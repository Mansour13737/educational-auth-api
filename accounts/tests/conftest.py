import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Fresh DRF test client for every test."""
    return APIClient()


@pytest.fixture
def registered_user(api_client):
    """A user already registered — used by login/profile tests."""
    payload = {
        "email": "fixture@example.com",
        "first_name": "Fixture",
        "last_name": "User",
        "password": "TestPass123",
        "password_confirm": "TestPass123",
    }
    response = api_client.post("/api/auth/register/", payload, format="json")
    assert response.status_code == 201
    return payload
