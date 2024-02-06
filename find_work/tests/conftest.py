from uuid import uuid4

import pyotp

import pytest

from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.test import APIClient

from cryptography.fernet import Fernet

from find_work.settings import (
    CRYPTOGRAPHY_FERNET_KEY
)

from user.models import (
    User,
    Profile,
)

from resume.models import (
    Skill,
    Resume,
    WorkExperience,
    Specialization,
    TypeOfEmployment,
)

from company.models import Company

pytest_plugins = [
    "tests.fixtures.fixtures_user_api.fixtures_login_user",
    "tests.fixtures.fixtures_user_api.fixtures_update_email",
    "tests.fixtures.fixtures_user_api.fixtures_upload_avatar",
    "tests.fixtures.fixtures_user_api.fixtures_reset_password",
    "tests.fixtures.fixtures_user_api.fixtures_update_password",
    "tests.fixtures.fixtures_user_api.fixtures_register_new_user",
    "tests.fixtures.fixtures_user_api.fixtures_activate_new_user",
    "tests.fixtures.fixtures_user_api.fixtures_validate_password",
    "tests.fixtures.fixtures_user_api.fixtures_edit_profile_info",
    "tests.fixtures.fixtures_user_api.fixtures_validate_totp_token",
    "tests.fixtures.fixtures_user_api.fixtures_enable_two_factor_auth",
    "tests.fixtures.fixtures_user_api.fixtures_disable_two_factor_auth",
    "tests.fixtures.fixtures_user_api.fixtures_generate_reset_password_totp",
    "tests.fixtures.fixtures_user_api.fixtures_validate_reset_password_totp",

    "tests.fixtures.fixtures_resume_api.fixtures_create_resume",
    "tests.fixtures.fixtures_resume_api.fixtures_edit_resume_info",

    "tests.fixtures.fixtures_company_api.fixtures_create_company",
    "tests.fixtures.fixtures_company_api.fixtures_edit_company_info",
]


@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture()
def create_new_user():
    profile = Profile(
        first_name="Ran",
        last_name="Goose",
    )
    profile.save()

    fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
    user_otp_base32 = pyotp.random_base32()
    user_encrypted_opt_base32 = fernet.encrypt(user_otp_base32.encode())

    user = User(
        email="raNGoose@email.com",
        user_activation_uuid=uuid4(),
        profile=profile,
        is_employer=True,
        is_employee=True,
        password=make_password("password"),
        otp_base32=user_encrypted_opt_base32.decode()
    )
    user.save()

    return user


@pytest.fixture
def user_obtain_token(
    client,
    create_new_user
):
    create_new_user.is_active = True
    create_new_user.save()

    data = {
        "email": create_new_user.email,
        "password": "password"
    }

    request = client.post(
        reverse("user_api:login_user"),
        data=data
    )

    return request.data


@pytest.fixture
def user_auth_headers(user_obtain_token):

    access_token = user_obtain_token["access"]

    authorization = {"Authorization": f"Bearer {access_token}"}

    return authorization


@pytest.fixture
def create_company(create_new_user):
    new_company = Company.objects.create(
        name="Test",
        author=create_new_user
    )

    return new_company


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
        create_skill,
        create_new_user,
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


@pytest.fixture()
def get_resume_id(create_resume):
    kwargs = {
        "resume_id": create_resume.pk
    }
    return kwargs


@pytest.fixture()
def get_wrong_resume_id():
    kwargs = {
        "resume_id": 0
    }
    return kwargs


@pytest.fixture()
def get_company_id(create_company):
    kwargs = {
        "company_id": create_company.pk
    }
    return kwargs


@pytest.fixture()
def get_wrong_company_id():
    kwargs = {
        "company_id": 0
    }
    return kwargs
