import pyotp

import pytest

from cryptography.fernet import Fernet

from find_work.settings import (
    CRYPTOGRAPHY_FERNET_KEY
)


@pytest.fixture()
def data_to_validate_totp_token(create_new_user):

    fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
    user_otp_base32 = fernet.decrypt(create_new_user.otp_base32.encode())

    totp = pyotp.TOTP(user_otp_base32.decode())

    data = {
        "totp_token": totp.now()
    }
    return data


@pytest.fixture()
def validate_totp_token_data_to_response_wrong_totp_token_error(
        create_new_user
):
    fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
    user_otp_base32 = fernet.decrypt(create_new_user.otp_base32.encode())

    totp = pyotp.TOTP(user_otp_base32)
    wrong_totp_token = int(totp.now()) - 1

    data = {
        "totp_token": wrong_totp_token
    }
    return data
