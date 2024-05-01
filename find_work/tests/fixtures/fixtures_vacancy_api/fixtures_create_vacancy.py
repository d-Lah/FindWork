import pytest


@pytest.fixture()
def data_to_create_vacancy(
        create_skill,
        create_specialization,
        create_work_experience,
        create_type_of_employment
):

    data = {
        "title": "Test",
        "body": "Test",
        "rqd_specialization": create_specialization.pk,
        "rqd_work_experience": create_work_experience.pk,
        "rqd_skill": [create_skill.pk],
        "rqd_type_of_employment": [create_type_of_employment.pk]
    }

    return data


@pytest.fixture()
def data_to_create_vacancy_wo_data(
    create_specialization,
    create_work_experience
):

    data = {
        "title": "",
        "body": "",
        "rqd_specialization": 1,
        "rqd_work_experience": 1,
        "rqd_skill": [],
        "rqd_type_of_employment": []
    }

    return data


@pytest.fixture()
def data_to_create_vacancy_w_not_exists_fields():

    data = {
        "title": "Test",
        "body": "Test",
        "rqd_specialization": 1,
        "rqd_work_experience": 1,
        "rqd_skill": [1],
        "rqd_type_of_employment": [1]
    }

    return data
