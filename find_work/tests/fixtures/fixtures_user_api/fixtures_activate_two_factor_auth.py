import pytest

from django.urls import reverse


@pytest.fixture()
def data_for_response_two_factor_auth_already_active_error(
        client,
        create_new_user,
):
    create_new_user.is_two_factor_auth = True
    create_new_user.is_active = True
    create_new_user.save()

    data = {
        "email": create_new_user.email,
        "password": "password"
    }
    request = client.post(
        reverse("user_api:login_user"),
        data=data
    )
    access_token = request.data["access"]

    authorization = {"Authorization": f"Bearer {access_token}"}

    return authorization
