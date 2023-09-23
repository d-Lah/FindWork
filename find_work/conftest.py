import pytest
from uuid import (
    uuid4,
)
from django.urls import (
    reverse,
)
from find_work.settings import (
    BASE_DIR,
)
from rest_framework.test import (
    APIClient,
)
from django.contrib.auth.hashers import (
    make_password,
)
from user.models import (
    User,
    Profile,
    UserAvatar,
    EmployerProfile,
    EmployeeProfile,
)


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


@pytest.fixture()
def data_for_test_activate_user(create_new_user):
    return create_new_user.user_activation_uuid


@pytest.fixture()
def data_for_test_user_already_active(create_new_user):
    create_new_user.is_active = True
    create_new_user.save()

    return create_new_user.user_activation_uuid
