import pytest


@pytest.fixture()
def data_for_test_should_generate_user_reset_password_totp(
    create_new_user
):
    create_new_user.is_active = True
    create_new_user.save()

    data = {
        "email": create_new_user.email
    }

    return data


@pytest.fixture()
def generate_user_reset_password_totp_data_for_response_user_not_found_error():
    data = {
        "email": "randomemail1234@email.com"
    }

    return data
