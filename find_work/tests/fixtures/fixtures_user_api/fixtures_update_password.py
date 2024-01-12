import pytest


@pytest.fixture()
def data_to_update_password():
    data = {
        "password": "new_password"
    }

    return data
