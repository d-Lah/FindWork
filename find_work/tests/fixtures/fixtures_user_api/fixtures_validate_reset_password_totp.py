import time

import pyotp

import pytest

from cryptography.fernet import Fernet

from find_work.settings import CRYPTOGRAPHY_FERNET_KEY


@pytest.fixture()
def data_to_validate_reset_password_totp(create_new_user):
    fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
    user_otp_base32 = fernet.decrypt(create_new_user.otp_base32.encode())

    totp = pyotp.TOTP(
        s=user_otp_base32,
        interval=172880
    )
    reset_password_totp = totp.now()

    data = {
        "email": create_new_user.email,
        "reset_password_totp": reset_password_totp
    }

    return data


@pytest.fixture()
def data_to_validate_reset_password_totp_wo_data():

    data = {
        "email": "",
        "reset_password_totp": ""
    }

    return data


@pytest.fixture()
def data_to_validate_reset_password_totp_w_wrong_email(
        create_new_user
):
    fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
    user_otp_base32 = fernet.decrypt(create_new_user.otp_base32.encode())

    totp = pyotp.TOTP(
        s=user_otp_base32,
        interval=172880
    )
    reset_password_totp = totp.now()

    data = {
        "email": "randomEmail@email.com",
        "reset_password_totp": reset_password_totp
    }

    return data


@pytest.fixture()
def data_to_validate_reset_password_totp_w_incap_reset_password_totp(
    create_new_user
):
    fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
    user_otp_base32 = fernet.decrypt(create_new_user.otp_base32.encode())

    totp = pyotp.TOTP(
        s=user_otp_base32,
        interval=0.001
    )
    reset_password_totp = totp.now()

    data = {
        "email": create_new_user.email,
        "reset_password_totp": reset_password_totp
    }

    time.sleep(0.001)

    return data
