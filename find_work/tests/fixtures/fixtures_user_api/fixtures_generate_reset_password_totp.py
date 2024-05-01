import pytest


@pytest.fixture()
def data_to_generate_reset_password_totp(
    create_user
):
    create_user.is_active = True
    create_user.save()

    data = {
        "email": create_user.email
    }

    return data


@pytest.fixture()
def data_to_generate_reset_password_totp_wo_email(
    create_user
):
    create_user.is_active = True
    create_user.save()

    data = {
        "email": ""
    }

    return data


@pytest.fixture()
def data_to_generate_reset_password_totp_w_invalid_email(
    create_user
):
    create_user.is_active = True
    create_user.save()

    data = {
        "email": "invalid_email_email_com"
    }

    return data


@pytest.fixture()
def data_to_generate_reset_password_totp_w_wrong_email():
    data = {
        "email": "wrong_email@email.com"
    }

    return data
