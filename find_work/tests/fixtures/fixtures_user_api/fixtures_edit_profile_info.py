import pytest


@pytest.fixture()
def data_to_edit_profile_info():
    data = {
        "first_name": "Lui",
        "last_name": "Onir"
    }
    return data


@pytest.fixture()
def data_to_edit_profile_info_wo_data():
    data = {
        "first_name": "",
        "last_name": ""
    }
    return data
