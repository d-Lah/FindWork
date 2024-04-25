import pytest


@pytest.fixture()
def data_to_create_resume(
        create_skill,
        create_specialization,
        create_work_experience,
        create_type_of_employment
):

    data = {
        "about": "Test",
        "specialization": create_specialization.pk,
        "work_experience": create_work_experience.pk,
        "skill": [create_skill.pk],
        "type_of_employment": [create_type_of_employment.pk]
    }

    return data


@pytest.fixture()
def data_to_create_resume_wo_data(
        create_specialization,
        create_work_experience
):

    data = {
        "about": "",
        "specialization": 1,
        "work_experience": 1,
        "skill": [],
        "type_of_employment": []
    }

    return data


@pytest.fixture()
def data_to_create_resume_w_wrong_specialization(
        create_skill,
        create_work_experience,
        create_type_of_employment,
):

    data = {
        "about": "Test",
        "specialization": 1,
        "work_experience": create_work_experience.pk,
        "skill": [create_skill.pk],
        "type_of_employment": [create_type_of_employment.pk]
    }

    return data


@pytest.fixture()
def data_to_create_resume_w_wrong_skill(
        create_specialization,
        create_work_experience,
        create_type_of_employment
):

    data = {
        "about": "Test",
        "specialization": create_specialization.pk,
        "work_experience": create_work_experience.pk,
        "skill": [1],
        "type_of_employment": [create_type_of_employment.pk]
    }

    return data


@pytest.fixture()
def data_to_create_resume_w_wrong_work_experience(
        create_skill,
        create_specialization,
        create_type_of_employment
):

    data = {
        "about": "Test",
        "specialization": create_specialization.pk,
        "work_experience": 1,
        "skill": [create_skill.pk],
        "type_of_employment": [create_type_of_employment.pk]
    }

    return data


@pytest.fixture()
def data_to_create_resume_w_wrong_type_of_employment(
        create_skill,
        create_specialization,
        create_work_experience,
):

    data = {
        "about": "Test",
        "specialization": create_specialization.pk,
        "work_experience": create_work_experience.pk,
        "skill": [create_skill.pk],
        "type_of_employment": [1]
    }

    return data
