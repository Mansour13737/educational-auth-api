import pytest


@pytest.mark.django_db
def test_register_success(api_client):
    payload = {
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "StrongPass123",
        "password_confirm": "StrongPass123",
    }
    response = api_client.post("/api/auth/register/", payload, format="json")
    assert response.status_code == 201
    assert response.json()["email"] == "newuser@example.com"
    assert "id" in response.json()


@pytest.mark.django_db
def test_register_duplicate_email(api_client, registered_user):
    # `registered_user` already created fixture@example.com
    payload = {
        "email": "fixture@example.com",
        "password": "AnotherPass123",
        "password_confirm": "AnotherPass123",
    }
    response = api_client.post("/api/auth/register/", payload, format="json")
    assert response.status_code == 400
    assert "email" in response.json()


@pytest.mark.django_db
def test_register_password_mismatch(api_client):
    payload = {
        "email": "mismatch@example.com",
        "password": "StrongPass123",
        "password_confirm": "DifferentPass123",
    }
    response = api_client.post("/api/auth/register/", payload, format="json")
    assert response.status_code == 400
    assert "password" in response.json()


@pytest.mark.django_db
def test_register_missing_fields(api_client):
    response = api_client.post("/api/auth/register/", {}, format="json")
    assert response.status_code == 400
    body = response.json()
    assert "email" in body
    assert "password" in body


@pytest.mark.django_db
def test_register_password_not_in_response(api_client):
    payload = {
        "email": "leakcheck@example.com",
        "password": "StrongPass123",
        "password_confirm": "StrongPass123",
    }
    response = api_client.post("/api/auth/register/", payload, format="json")
    assert response.status_code == 201
    body = response.json()
    assert "password" not in body
    assert "password_confirm" not in body