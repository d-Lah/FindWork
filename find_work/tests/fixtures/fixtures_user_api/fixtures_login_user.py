import pytest


@pytest.fixture()
def data_for_login_user(create_new_user):
    create_new_user.is_active = True
    create_new_user.save()

    data = {
        "email": create_new_user.email,
        "password": "password"
    }
    return data


@pytest.fixture()
def login_user_data_for_response_user_not_active_error(create_new_user):
    data = {
        "email": create_new_user.email,
        "password": "password"
    }
    return data


@pytest.fixture()
def login_user_data_for_response_email_field_empty_error(
):
    data = {
        "email": "",
        "password": "password"
    }

    return data


@pytest.fixture()
def login_user_data_for_response_password_field_empty_error(
        create_new_user,
):
    data = {
        "email": create_new_user.email,
        "password": ""
    }

    return data


@pytest.fixture()
def login_user_data_for_response_user_not_found_error_cause_wrong_email():
    data = {
        "email": "wrong_email@email.com",
        "password": "password"
    }

    return data


@pytest.fixture()
def login_user_data_for_response_user_not_found_error_cause_wrong_password(
        create_new_user,
):
    create_new_user.is_active = True
    create_new_user.save()

    data = {
        "email": create_new_user.email,
        "password": "wrong_password"
    }

    return data
