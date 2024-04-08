import pytest


@pytest.fixture()
def data_to_update_resume_info(
        create_skill,
        create_user,
        create_specialization,
        create_work_experience,
        create_type_of_employment
):

    data = {
        "about": "Test 2",
        "specialization": create_specialization.pk,
        "work_experience": create_work_experience.pk,
        "skill": [create_skill.pk],
        "type_of_employment": [create_type_of_employment.pk]
    }

    return data


@pytest.fixture()
def data_to_edit_resume_info_wo_data():

    data = {
        "about": "",
        "specialization": "",
        "work_experience": "",
        "skill": "",
        "type_of_employment": ""
    }

    return data


@pytest.fixture()
def data_to_edit_resume_info_w_wrong_specialization(
        create_skill,
        create_work_experience,
        create_type_of_employment,
):

    data = {
        "about": "Test",
        "specialization": 0,
        "work_experience": create_work_experience.pk,
        "skill": [create_skill.pk],
        "type_of_employment": [create_type_of_employment.pk]
    }

    return data


@pytest.fixture()
def data_to_edit_resume_info_w_wrong_skill(
        create_specialization,
        create_work_experience,
        create_type_of_employment
):

    data = {
        "about": "Test",
        "specialization": create_specialization.pk,
        "work_experience": create_work_experience.pk,
        "skill": [0],
        "type_of_employment": [create_type_of_employment.pk]
    }

    return data


@pytest.fixture()
def data_to_edit_resume_info_w_wrong_work_experience(
        create_skill,
        create_specialization,
        create_type_of_employment
):

    data = {
        "about": "Test",
        "specialization": create_specialization.pk,
        "work_experience": 0,
        "skill": [create_skill.pk],
        "type_of_employment": [create_type_of_employment.pk]
    }

    return data


@pytest.fixture()
def data_to_edit_resume_info_w_wrong_type_of_employment(
        create_skill,
        create_specialization,
        create_work_experience,
):

    data = {
        "about": "Test",
        "specialization": create_specialization.pk,
        "work_experience": create_work_experience.pk,
        "skill": [create_skill.pk],
        "type_of_employment": [0]
    }

    return data
