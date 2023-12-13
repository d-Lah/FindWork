import pytest


@pytest.fixture()
def check_user_password():
    data = {
        "password": "password"
    }
    return data


@pytest.fixture()
def check_user_password_response_wrong_password_error():
    data = {
        "password": "wrong_password"
    }

    return data
