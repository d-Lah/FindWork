import pytest


@pytest.fixture()
def data_to_update_resume_info():

    data = {
        "about": "Test 2",
        "specialization": 1,
        "work_experience": 1,
        "skill": [1],
        "type_of_employment": [1]
    }

    return data


@pytest.fixture()
def data_to_edit_resume_info_wo_data():

    data = {
        "about": "",
        "specialization": 1,
        "work_experience": 1,
        "skill": [],
        "type_of_employment": []
    }

    return data


@pytest.fixture()
def data_to_edit_resume_info_w_not_exists_field(
):

    data = {
        "about": "Test",
        "specialization": 2,
        "work_experience": 2,
        "skill": [2],
        "type_of_employment": [2]
    }

    return data
