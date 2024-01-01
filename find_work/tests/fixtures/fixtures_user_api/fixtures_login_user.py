import pytest


@pytest.fixture()
def data_to_login_user(create_new_user):
    create_new_user.is_active = True
    create_new_user.save()

    data = {
        "email": create_new_user.email,
        "password": "password"
    }
    return data


@pytest.fixture()
def data_to_login_user_w_not_active_user(create_new_user):
    data = {
        "email": create_new_user.email,
        "password": "password"
    }
    return data


@pytest.fixture()
def data_to_login_user_wo_email(
):
    data = {
        "email": "",
        "password": "password"
    }

    return data


@pytest.fixture()
def data_to_login_user_wo_password(
        create_new_user,
):
    data = {
        "email": create_new_user.email,
        "password": ""
    }

    return data


@pytest.fixture()
def data_to_login_user_w_wrong_email():
    data = {
        "email": "wrong_email@email.com",
        "password": "password"
    }

    return data


@pytest.fixture()
def data_to_login_user_w_wrong_password(
        create_new_user,
):
    create_new_user.is_active = True
    create_new_user.save()

    data = {
        "email": create_new_user.email,
        "password": "wrong_password"
    }

    return data
