import pytest


@pytest.fixture()
def data_to_login_user(create_user):
    create_user.is_active = True
    create_user.save()

    data = {
        "email": create_user.email,
        "password": "password"
    }
    return data


@pytest.fixture()
def data_to_login_user_w_not_active_user(create_user):
    data = {
        "email": create_user.email,
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
        create_user,
):
    data = {
        "email": create_user.email,
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
        create_user,
):
    create_user.is_active = True
    create_user.save()

    data = {
        "email": create_user.email,
        "password": "wrong_password"
    }

    return data
