import pytest


@pytest.fixture()
def data_for_test_should_update_user_password():
    data = {
        "password": "new_password"
    }

    return data
