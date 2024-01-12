import pytest


@pytest.fixture()
def data_to_validate_password():
    data = {
        "password": "password"
    }
    return data


@pytest.fixture()
def data_to_validate_password_w_wrong_password():
    data = {
        "password": "wrong_password"
    }

    return data
