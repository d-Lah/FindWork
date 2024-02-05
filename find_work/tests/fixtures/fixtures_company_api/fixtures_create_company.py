import pytest


@pytest.fixture
def data_to_create_company():
    data = {
        "name": "Test"
    }

    return data


@pytest.fixture
def data_to_create_company_wo_data():
    data = {
        "name": ""
    }

    return data


@pytest.fixture
def data_to_create_company_w_already_exists_name(create_company):
    data = {
        "name": create_company.name
    }

    return data
