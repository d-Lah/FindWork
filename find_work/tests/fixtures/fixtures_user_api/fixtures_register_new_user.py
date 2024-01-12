import pytest


@pytest.fixture()
def data_to_register_new_user():
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
def data_to_register_new_user_wo_data():
    data = {
        "email": "",
        "phone_number": "",
        "password": "",
        "is_employer": "",
        "is_employee": "",
        "first_name": "",
        "second_name": "",
    }
    return data


@pytest.fixture()
def data_to_register_new_user_w_invalid_email(
        create_new_user,
):
    data = {
        "email": "invalid_email_email_com",
        "phone_number": "12344321",
        "password": "password",
        "is_employer": False,
        "is_employee": True,
        "first_name": "Mykola",
        "second_name": "Mleko",
    }
    return data


@pytest.fixture()
def data_to_register_new_user_w_already_exists_email(
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
