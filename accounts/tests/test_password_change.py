import pytest

from accounts.models import User


def _login_and_auth(api_client, email, password):
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
def test_change_password_requires_auth(api_client):
    response = api_client.post(
        "/api/auth/change-password/",
        {
            "old_password": "TestPass123",
            "new_password": "NewPass456",
            "new_password_confirm": "NewPass456",
        },
        format="json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_change_password_wrong_old(api_client, registered_user):
    _login_and_auth(api_client, registered_user["email"], registered_user["password"])
    response = api_client.post(
        "/api/auth/change-password/",
        {
            "old_password": "WrongOld999",
            "new_password": "NewPass456",
            "new_password_confirm": "NewPass456",
        },
        format="json",
    )
    assert response.status_code == 400
    assert "old_password" in response.json()


@pytest.mark.django_db
def test_change_password_mismatch_new(api_client, registered_user):
    _login_and_auth(api_client, registered_user["email"], registered_user["password"])
    response = api_client.post(
        "/api/auth/change-password/",
        {
            "old_password": registered_user["password"],
            "new_password": "NewPass456",
            "new_password_confirm": "Different789",
        },
        format="json",
    )
    assert response.status_code == 400
    assert "new_password" in response.json()


@pytest.mark.django_db
def test_change_password_success_and_login(api_client, registered_user):
    old_password = registered_user["password"]
    new_password = "BrandNewPass789"

    _login_and_auth(api_client, registered_user["email"], old_password)
    response = api_client.post(
        "/api/auth/change-password/",
        {
            "old_password": old_password,
            "new_password": new_password,
            "new_password_confirm": new_password,
        },
        format="json",
    )
    assert response.status_code == 200

    # Old password must now fail
    old_login = api_client.post(
        "/api/auth/login/",
        {"email": registered_user["email"], "password": old_password},
        format="json",
    )
    assert old_login.status_code == 401

    # New password must now succeed
    new_login = api_client.post(
        "/api/auth/login/",
        {"email": registered_user["email"], "password": new_password},
        format="json",
    )
    assert new_login.status_code == 200
    assert "access" in new_login.json()


@pytest.mark.django_db
def test_change_password_hashes_new_password(api_client, registered_user):
    new_password = "HashedPass321"
    _login_and_auth(api_client, registered_user["email"], registered_user["password"])
    response = api_client.post(
        "/api/auth/change-password/",
        {
            "old_password": registered_user["password"],
            "new_password": new_password,
            "new_password_confirm": new_password,
        },
        format="json",
    )
    assert response.status_code == 200

    user = User.objects.get(email=registered_user["email"])
    # Stored value must NOT be the plaintext password
    assert user.password != new_password
    # And it must look like a Django hash
    assert user.password.startswith(("pbkdf2_", "argon2"))
    # check_password still verifies the original value
    assert user.check_password(new_password) is True