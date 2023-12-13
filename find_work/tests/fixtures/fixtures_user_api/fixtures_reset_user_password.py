import pytest


@pytest.fixture()
def data_to_reset_user_password(create_new_user):
    data = {
        "email": create_new_user.email,
        "password": "new_password"
    }
    return data


@pytest.fixture()
def reset_user_password_data_to_response_email_field_empty_error(
        create_new_user
):
    data = {
        "password": "new_password"
    }
    return data


@pytest.fixture()
def reset_user_password_data_to_response_password_field_empty_error(
        create_new_user
):
    data = {
        "email": create_new_user.email,
    }
    return data


@pytest.fixture()
def reset_user_password_data_to_response_user_not_found_error():
    data = {
        "email": "randomEmail@email.com",
        "password": "new_password"
    }
    return data
