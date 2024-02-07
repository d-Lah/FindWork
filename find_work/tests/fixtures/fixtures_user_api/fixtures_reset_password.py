import pytest


@pytest.fixture()
def data_to_reset_password(create_new_user):
    data = {
        "email": create_new_user.email,
        "password": "new_password"
    }
    return data


@pytest.fixture()
def data_to_reset_password_wo_data():
    data = {
        "email": "",
        "password": ""
    }
    return data


@pytest.fixture()
def data_to_reset_password_w_invalid_email():
    data = {
        "email": "invalid_email_email_com",
        "password": "new_password"
    }

    return data


@pytest.fixture()
def data_to_reset_password_w_wrong_email():
    data = {
        "email": "randomEmail@email.com",
        "password": "new_password"
    }
    return data
