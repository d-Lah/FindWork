import pytest


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
def register_new_user_data_for_response_email_field_empty_error():
    data = {
        "email": "",
        "phone_number": "12344321",
        "password": "password",
        "is_employer": False,
        "is_employee": True,
        "first_name": "Mykola",
        "second_name": "Mleko",
    }
    return data


@pytest.fixture()
def register_new_user_data_for_response_phone_number_field_empty_error():
    data = {
        "email": "test@email.com",
        "phone_number": "",
        "password": "password",
        "is_employer": False,
        "is_employee": True,
        "first_name": "Mykola",
        "second_name": "Mleko",
    }
    return data


@pytest.fixture()
def register_new_user_data_for_response_password_field_empty_error():
    data = {
        "email": "test@email.com",
        "phone_number": "12344321",
        "password": "",
        "is_employer": False,
        "is_employee": True,
        "first_name": "Mykola",
        "second_name": "Mleko",
    }
    return data


@pytest.fixture()
def register_new_user_data_for_response_is_employer_field_empty_error():
    data = {
        "email": "test@email.com",
        "phone_number": "12344321",
        "password": "password",
        "is_employer": "",
        "is_employee": True,
        "first_name": "Mykola",
        "second_name": "Mleko",
    }
    return data


@pytest.fixture()
def register_new_user_data_for_response_is_employee_field_empty_error():
    data = {
        "email": "test@email.com",
        "phone_number": "12344321",
        "password": "password",
        "is_employer": False,
        "is_employee": "",
        "first_name": "Mykola",
        "second_name": "Mleko",
    }
    return data


@pytest.fixture()
def register_new_user_data_for_response_first_name_field_empty_error():
    data = {
        "email": "test@email.com",
        "phone_number": "12344321",
        "password": "password",
        "is_employer": False,
        "is_employee": True,
        "first_name": "",
        "second_name": "Mleko",
    }
    return data


@pytest.fixture()
def register_new_user_data_for_response_second_name_field_empty_error():
    data = {
        "email": "test@email.com",
        "phone_number": "12344321",
        "password": "password",
        "is_employer": False,
        "is_employee": True,
        "first_name": "Mykola",
        "second_name": "",
    }
    return data


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
