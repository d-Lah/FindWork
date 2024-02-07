import pytest


@pytest.fixture()
def data_to_update_email():
    data = {
        "email": "new_email@email.com"
    }

    return data


@pytest.fixture()
def data_to_update_email_wo_email():
    data = {
        "email": ""
    }

    return data


@pytest.fixture()
def data_to_update_email_w_invalid_email():
    data = {
        "email": "invalid_email_email_com"
    }

    return data


@pytest.fixture()
def data_to_update_email_w_already_exists_email(
        create_new_user
):
    data = {
        "email": create_new_user.email
    }

    return data
