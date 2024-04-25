import pytest


@pytest.fixture()
def data_to_update_password():
    data = {
        "old_password": "password",
        "new_password": "new_password"
    }

    return data


@pytest.fixture()
def data_to_update_password_wo_data():
    data = {
        "old_password": "",
        "new_password": ""
    }

    return data


@pytest.fixture()
def data_to_update_password_w_wrong_old_password():
    data = {
        "old_password": "wrong_password",
        "new_password": "new_password"
    }

    return data
