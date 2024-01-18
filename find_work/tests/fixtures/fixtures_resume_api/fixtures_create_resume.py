import pytest
from resume.models import (
    Skill,
    WorkExperience,
    Specialization,
    TypeOfEmployment,
)


@pytest.fixture()
def create_specialization():
    specialization = Specialization.objects.create(
        specialization_name="Python"
    )
    return specialization


@pytest.fixture()
def create_skill():
    skill = Skill.objects.create(
        skill_name="Django"
    )
    return skill


@pytest.fixture()
def create_work_experience():
    work_experience = WorkExperience.objects.create(
        work_experience_name="1 year"
    )
    return work_experience


@pytest.fixture()
def create_type_of_employment():
    type_of_employment = TypeOfEmployment.objects.create(
        type_of_employment_name="Part-time"
    )
    return type_of_employment


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
def data_to_create_resume_wo_data():

    data = {
        "about": "",
        "specialization": "",
        "work_experience": "",
        "skill": "",
        "type_of_employment": ""
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
