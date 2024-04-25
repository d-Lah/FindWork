import pyotp

import pytest

from cryptography.fernet import Fernet

from find_work.settings import (
    CRYPTOGRAPHY_FERNET_KEY
)


@pytest.fixture()
def data_to_validate_totp(create_user):

    fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
    user_otp_base32 = fernet.decrypt(create_user.otp_base32.encode())

    totp = pyotp.TOTP(user_otp_base32.decode())

    data = {
        "totp": totp.now()
    }
    return data


@pytest.fixture()
def data_to_validate_totp_w_totp_incap(
        create_user
):
    fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
    user_otp_base32 = fernet.decrypt(create_user.otp_base32.encode())

    totp = pyotp.TOTP(user_otp_base32)
    wrong_totp_token = int(totp.now()) - 1

    data = {
        "totp": wrong_totp_token
    }
    return data


@pytest.fixture()
def data_to_validate_totp_wo_data():
    data = {
        "totp": ""
    }
    return data
