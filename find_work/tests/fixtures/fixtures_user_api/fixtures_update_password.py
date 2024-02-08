import pytest


@pytest.fixture()
def data_to_update_password():
    data = {
        "password": "new_password"
    }

    return data


@pytest.fixture()
def data_to_update_password_wo_data():
    data = {
        "password": ""
    }

    return data
