import pytest


@pytest.fixture()
def data_for_activate_new_user(create_new_user):
    kwargs = {
        "user_activation_uuid": create_new_user.user_activation_uuid
    }
    return kwargs


@pytest.fixture()
def activate_new_user_data_for_response_user_already_active_error(
        create_new_user
):
    create_new_user.is_active = True
    create_new_user.save()

    kwargs = {
        "user_activation_uuid": create_new_user.user_activation_uuid
    }
    return kwargs
