from uuid import uuid4

import pyotp
import pytest

from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.test import APIClient

from user.models import (
    User,
    Profile,
    UserAvatar,
    EmployerProfile,
    EmployeeProfile,
)
from find_work.settings import BASE_DIR


@pytest.fixture
def client():
    client = APIClient()
    return client


# Fixtures for register api


@pytest.fixture()
def data_for_test_register_user():
    data = {
        "email": "test@email.com",
        "phone_number": "12344321",
        "password": "password",
        "is_employer": False,
        "is_employee": True,
        "first_name": "Mykola",
        "second_name": "Mleko",
    }
    return data


@pytest.fixture()
def data_for_test_user_field_empty_error():
    data = {
        "email": "",
        "phone_number": "",
        "password": "",
        "is_employer": "",
        "is_employee": "",
        "first_name": "Mykola",
        "second_name": "Mleko",
    }
    return data


@pytest.fixture()
def data_for_test_profile_field_empty_error():
    data = {
        "email": "test@email.com",
        "phone_number": "12344321",
        "password": "password",
        "is_employer": False,
        "is_employee": True,
        "first_name": "",
        "second_name": "",
    }
    return data


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

    user = User(
        email="raNGoose@email.com",
        phone_number="380321124353",
        user_activation_uuid=uuid4(),
        profile=profile,
        is_employer=False,
        is_employee=True,
        password=make_password("password"),
    )
    user.save()

    return user


@pytest.fixture()
def data_for_test_email_already_exists_error(
        create_new_user,
):
    data = {
        "email": create_new_user.email,
        "phone_number": "12344321",
        "password": "password",
        "is_employer": False,
        "is_employee": True,
        "first_name": "Mykola",
        "second_name": "Mleko",
    }
    return data


@pytest.fixture()
def data_for_test_phone_number_already_exists_error(
        create_new_user,
):
    data = {
        "email": "RangoosE@email.com",
        "phone_number": create_new_user.phone_number,
        "password": "password",
        "is_employer": False,
        "is_employee": True,
        "first_name": "Mykola",
        "second_name": "Mleko",
    }
    return data


# Fixtures for activate user api


@pytest.fixture()
def data_for_test_activate_user(create_new_user):
    return create_new_user.user_activation_uuid


@pytest.fixture()
def data_for_test_user_already_active_error(create_new_user):
    create_new_user.is_active = True
    create_new_user.save()

    return create_new_user.user_activation_uuid


# Fixtures for login api


@pytest.fixture()
def data_for_test_login_user(create_new_user):
    create_new_user.is_active = True
    create_new_user.save()

    data = {
        "email": create_new_user.email,
        "password": "password"
    }
    return data


@pytest.fixture()
def data_for_test_response_user_not_active_error(create_new_user):
    data = {
        "email": create_new_user.email,
        "password": "password"
    }
    return data


@pytest.fixture()
def data_for_test_response_field_empty_error():
    data = {
        "email": "",
        "password": ""
    }
    return data


@pytest.fixture
def user_obtain_token(
    client,
    data_for_test_login_user
):
    responce = client.post(
        reverse("user_api:login"),
        data_for_test_login_user
    )

    return responce.data


@pytest.fixture
def user_auth_headers(user_obtain_token):

    access_token = user_obtain_token["access"]

    authorization = {"Authorization": f"Bearer {access_token}"}

    return authorization


@pytest.fixture()
def data_for_test_should_create_two_factor_auth_qr_code(create_new_user):
    create_new_user.is_active = True
    create_new_user.save()

    data = {
        "user_id": create_new_user.id,
    }
    return data


@pytest.fixture()
def set_base32_for_user(create_new_user):
    otp_base32 = pyotp.random_base32()
    create_new_user.otp_base32 = otp_base32
    create_new_user.save()

    return create_new_user


@pytest.fixture()
def data_for_test_validate_totp_token(
    set_base32_for_user
):
    user = set_base32_for_user

    totp = pyotp.TOTP(user.otp_base32)

    data = {
        "user_id": user.id,
        "totp_token": totp.now()
    }
    return data


@pytest.fixture()
def data_for_test_should_response_user_not_found_error(
    set_base32_for_user
):
    user = set_base32_for_user

    totp = pyotp.TOTP(user.otp_base32)

    data = {
        "totp_token": totp.now()
    }
    return data


@pytest.fixture()
def data_for_test_should_response_wrong_totp_token_error(
    set_base32_for_user
):
    user = set_base32_for_user

    totp = pyotp.TOTP(user.otp_base32)
    wrong_totp_token = int(totp.now()) - 1

    data = {
        "user_id": user.id,
        "totp_token": wrong_totp_token
    }
    return data


@pytest.fixture()
def data_for_test_should_edit_profile_info():
    data = {
        "first_name": "Lui",
        "second_name": "Onir"
    }
    return data


@pytest.fixture()
def data_for_test_should_check_user_password():
    data = {
        "password": "password"
    }
    return data


@pytest.fixture()
def data_for_test_should_response_wrong_password_error():
    data = {
        "password": "wrong_password"
    }

    return data


@pytest.fixture()
def data_for_test_should_update_user_password():
    data = {
        "password": "new_password"
    }

    return data
