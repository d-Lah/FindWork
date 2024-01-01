import pytest


@pytest.fixture()
def data_to_update_phone_number():
    data = {
        "phone_number": "1234554321"
    }

    return data


@pytest.fixture()
def data_to_update_phone_number_wo_phone_number():
    data = {
        "phone_number": ""
    }

    return data


@pytest.fixture()
def data_to_update_phone_number_w_already_exists_phone_number(
        create_new_user
):
    data = {
        "phone_number": create_new_user.phone_number
    }

    return data
