import pytest


@pytest.mark.django_db
def test_login_success(api_client, registered_user):
    response = api_client.post(
        "/api/auth/login/",
        {"email": registered_user["email"], "password": registered_user["password"]},
        format="json",
    )
    assert response.status_code == 200
    body = response.json()
    assert "access" in body
    assert "refresh" in body


@pytest.mark.django_db
def test_login_wrong_password(api_client, registered_user):
    response = api_client.post(
        "/api/auth/login/",
        {"email": registered_user["email"], "password": "WrongPassword999"},
        format="json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_login_unknown_email(api_client):
    response = api_client.post(
        "/api/auth/login/",
        {"email": "nobody@example.com", "password": "AnyPass123"},
        format="json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_login_response_shape(api_client, registered_user):
    response = api_client.post(
        "/api/auth/login/",
        {"email": registered_user["email"], "password": registered_user["password"]},
        format="json",
    )
    assert response.status_code == 200
    assert set(response.json().keys()) == {"access", "refresh"}


@pytest.mark.django_db
def test_login_access_token_works(api_client, registered_user):
    login = api_client.post(
        "/api/auth/login/",
        {"email": registered_user["email"], "password": registered_user["password"]},
        format="json",
    )
    access = login.json()["access"]

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    profile = api_client.get("/api/profile/")
    assert profile.status_code == 200
    assert profile.json()["email"] == registered_user["email"]
