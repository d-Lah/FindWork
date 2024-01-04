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
    EmployeeProfile,
)
pytest_plugins = [
    "tests.fixtures.fixtures_user_api.fixtures_activate_new_user",
    "tests.fixtures.fixtures_user_api.fixtures_activate_two_factor_auth",
    "tests.fixtures.fixtures_user_api.fixtures_validate_password",
    "tests.fixtures.fixtures_user_api.fixtures_edit_profile_info",
    "tests.fixtures.fixtures_user_api.fixtures_generate_reset_password_totp",
    "tests.fixtures.fixtures_user_api.fixtures_login_user",
    "tests.fixtures.fixtures_user_api.fixtures_register_new_user",
    "tests.fixtures.fixtures_user_api.fixtures_update_email",
    "tests.fixtures.fixtures_user_api.fixtures_update_password",
    "tests.fixtures.fixtures_user_api.fixtures_update_phone_number",
    "tests.fixtures.fixtures_user_api.fixtures_upload_avatar",
    "tests.fixtures.fixtures_user_api.fixtures_validate_totp_token",
    "tests.fixtures.fixtures_user_api.fixtures_validate_reset_password_totp",
    "tests.fixtures.fixtures_user_api.fixtures_reset_password",
    "tests.fixtures.fixtures_user_api.fixtures_deactivate_two_factor_auth",
]


@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture()
def create_new_user():
    employee_profile = EmployeeProfile()
    employee_profile.save()

    profile = Profile(
        first_name="Ran",
        second_name="Goose",
        employee_profile=employee_profile,
        employer_profile=None,
    )
    profile.save()

    fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
    user_otp_base32 = pyotp.random_base32()
    user_encrypted_opt_base32 = fernet.encrypt(user_otp_base32.encode())

    user = User(
        email="raNGoose@email.com",
        phone_number="380321124353",
        user_activation_uuid=uuid4(),
        profile=profile,
        is_employer=False,
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
