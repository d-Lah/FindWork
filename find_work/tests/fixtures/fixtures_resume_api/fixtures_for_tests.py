import pytest
from resume.models import (
    Skill,
    Resume,
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
def create_resume(
        create_new_user,
        create_skill,
        create_specialization,
        create_work_experience,
        create_type_of_employment
):
    new_resume = Resume.objects.create(
        author=create_new_user,
        about="Test",
        specialization=create_specialization,
        work_experience=create_work_experience,
    )
    new_resume.skill.add(create_skill)
    new_resume.type_of_employment.add(create_type_of_employment)

    return new_resume
