import pytest

from django.urls import reverse


@pytest.fixture()
def data_to_enable_two_factor_auth_w_already_enabled_auth(
        client,
        create_user,
):
    create_user.is_two_factor_auth = True
    create_user.is_active = True
    create_user.save()

    data = {
        "email": create_user.email,
        "password": "password"
    }
    request = client.post(
        reverse("user_api:login_user"),
        data=data
    )
    access_token = request.data["access"]

    authorization = {"Authorization": f"Bearer {access_token}"}

    return authorization
