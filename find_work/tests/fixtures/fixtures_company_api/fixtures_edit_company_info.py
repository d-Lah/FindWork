import pytest


@pytest.fixture
def data_to_edit_company_info():
    data = {
        "name": "Test2"
    }

    return data


@pytest.fixture
def data_to_edit_company_info_wo_data():
    data = {
        "name": ""
    }

    return data


@pytest.fixture
def data_to_edit_company_info_w_already_exists_name(create_company):
    data = {
        "name": create_company.name
    }

    return data
