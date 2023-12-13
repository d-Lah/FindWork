import pytest


@pytest.fixture()
def data_for_test_should_edit_profile_info():
    data = {
        "first_name": "Lui",
        "second_name": "Onir"
    }
    return data


@pytest.fixture()
def edit_profile_info_data_for_response_first_name_field_empty_error():
    data = {
        "first_name": "",
        "second_name": "Onir"
    }
    return data


@pytest.fixture()
def edit_profile_info_data_for_response_second_name_field_empty_error():
    data = {
        "first_name": "Lui",
        "second_name": ""
    }
    return data
