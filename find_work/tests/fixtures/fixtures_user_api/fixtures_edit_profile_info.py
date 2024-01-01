import pytest


@pytest.fixture()
def data_to_edit_profile_info():
    data = {
        "first_name": "Lui",
        "second_name": "Onir"
    }
    return data


@pytest.fixture()
def data_to_edit_profile_info_wo_data():
    data = {
        "first_name": "",
        "second_name": ""
    }
    return data
