import pytest


def _login(api_client, email, password):
    response = api_client.post(
        "/api/auth/login/",
        {"email": email, "password": password},
        format="json",
    )
    assert response.status_code == 200
    return response.json()


@pytest.mark.django_db
def test_logout_blacklists_refresh(api_client, registered_user):
    tokens = _login(api_client, registered_user["email"], registered_user["password"])
    refresh = tokens["refresh"]

    # Logout
    response = api_client.post(
        "/api/auth/logout/",
        {"refresh": refresh},
        format="json",
    )
    assert response.status_code == 200

    # Same refresh token must now be rejected
    retry = api_client.post(
        "/api/auth/refresh/",
        {"refresh": refresh},
        format="json",
    )
    assert retry.status_code == 401
    assert retry.json()["code"] == "token_not_valid"


@pytest.mark.django_db
def test_logout_requires_refresh_field(api_client, registered_user):
    _login(api_client, registered_user["email"], registered_user["password"])
    response = api_client.post("/api/auth/logout/", {}, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_refresh_rotation_invalidates_old_token(api_client, registered_user):
    tokens = _login(api_client, registered_user["email"], registered_user["password"])
    original_refresh = tokens["refresh"]

    # First refresh should succeed and issue new tokens
    first = api_client.post(
        "/api/auth/refresh/",
        {"refresh": original_refresh},
        format="json",
    )
    assert first.status_code == 200
    assert "access" in first.json()
    assert "refresh" in first.json()

    # Reusing the ORIGINAL refresh must now fail (rotation blacklisted it)
    second = api_client.post(
        "/api/auth/refresh/",
        {"refresh": original_refresh},
        format="json",
    )
    assert second.status_code == 401
    assert second.json()["code"] == "token_not_valid"


@pytest.mark.django_db
def test_logout_with_invalid_token(api_client, registered_user):
    _login(api_client, registered_user["email"], registered_user["password"])
    response = api_client.post(
        "/api/auth/logout/",
        {"refresh": "not.a.real.token"},
        format="json",
    )
    assert response.status_code == 401