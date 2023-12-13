import pytest


@pytest.fixture()
def data_for_test_should_update_user_phone_number():
    data = {
        "phone_number": "1234554321"
    }

    return data


@pytest.fixture()
def update_phone_number_data_for_respons_phone_number_already_exists(
        create_new_user
):
    data = {
        "phone_number": create_new_user.phone_number
    }

    return data
