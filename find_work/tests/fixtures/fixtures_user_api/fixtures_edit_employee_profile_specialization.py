import pytest

from user.models import EmployeeSpecialization


@pytest.fixture()
def data_to_edit_employee_profile_specialization():
    new_employee_specialization = EmployeeSpecialization(name="Python")

    new_employee_specialization.save()

    data = {
        "id": new_employee_specialization.id,
        "name": new_employee_specialization.name
    }
    return data


@pytest.fixture()
def data_to_edit_employee_profile_specialization_wo_data():
    data = {
        "id": "",
        "name": ""
    }
    return data


@pytest.fixture()
def data_to_edit_employee_profile_specialization_w_wrong_specialization():
    data = {
        "id": "0",
        "name": "Null"
    }
    return data
