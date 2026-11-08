import pytest


def _login_and_auth(api_client, email, password):
    """Helper: log in and set the bearer header on the client."""
    response = api_client.post(
        "/api/auth/login/",
        {"email": email, "password": password},
        format="json",
    )
    assert response.status_code == 200
    access = response.json()["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return api_client


@pytest.mark.django_db
def test_profile_requires_auth(api_client):
    response = api_client.get("/api/profile/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_profile_returns_own_data(api_client, registered_user):
    _login_and_auth(api_client, registered_user["email"], registered_user["password"])
    response = api_client.get("/api/profile/")
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == registered_user["email"]
    assert body["first_name"] == registered_user["first_name"]
    assert body["last_name"] == registered_user["last_name"]


@pytest.mark.django_db
def test_profile_does_not_leak_sensitive_fields(api_client, registered_user):
    _login_and_auth(api_client, registered_user["email"], registered_user["password"])
    response = api_client.get("/api/profile/")
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {"id", "email", "first_name", "last_name", "date_joined"}
    for forbidden in ("password", "is_staff", "is_superuser", "groups", "user_permissions"):
        assert forbidden not in body


@pytest.mark.django_db
def test_profile_patch_updates_fields(api_client, registered_user):
    _login_and_auth(api_client, registered_user["email"], registered_user["password"])
    response = api_client.patch(
        "/api/profile/",
        {"first_name": "Updated", "last_name": "Name"},
        format="json",
    )
    assert response.status_code == 200
    body = response.json()
    assert body["first_name"] == "Updated"
    assert body["last_name"] == "Name"


@pytest.mark.django_db
def test_profile_patch_cannot_change_email(api_client, registered_user):
    original_email = registered_user["email"]
    _login_and_auth(api_client, original_email, registered_user["password"])
    response = api_client.patch(
        "/api/profile/",
        {"email": "hacker@example.com"},
        format="json",
    )
    # Read-only fields are silently ignored — response stays 200
    assert response.status_code == 200
    assert response.json()["email"] == original_email


@pytest.mark.django_db
def test_profile_isolation_between_users(api_client, registered_user):
    # Create a second user
    second_payload = {
        "email": "second@example.com",
        "first_name": "Second",
        "last_name": "User",
        "password": "TestPass123",
        "password_confirm": "TestPass123",
    }
    api_client.post("/api/auth/register/", second_payload, format="json")

    # Log in as the first user, get profile — must be first user's data
    _login_and_auth(api_client, registered_user["email"], registered_user["password"])
    response_a = api_client.get("/api/profile/")
    assert response_a.status_code == 200
    assert response_a.json()["email"] == registered_user["email"]

    # Log in as second user — must be second user's data
    _login_and_auth(api_client, second_payload["email"], second_payload["password"])
    response_b = api_client.get("/api/profile/")
    assert response_b.status_code == 200
    assert response_b.json()["email"] == second_payload["email"]
