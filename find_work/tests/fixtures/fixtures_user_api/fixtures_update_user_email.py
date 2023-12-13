import pytest


@pytest.fixture()
def data_for_test_should_update_user_email():
    data = {
        "email": "new_email@email.com"
    }

    return data


@pytest.fixture()
def update_user_email_data_for_response_email_already_exist_error(
        create_new_user
):
    data = {
        "email": create_new_user.email
    }

    return data
