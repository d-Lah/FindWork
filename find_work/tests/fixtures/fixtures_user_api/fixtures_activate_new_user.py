import pytest


@pytest.fixture()
def data_to_activate_new_user(create_new_user):
    kwargs = {
        "user_activation_uuid": create_new_user.user_activation_uuid
    }
    return kwargs


@pytest.fixture()
def data_to_activate_new_user_w_already_activate_user(
        create_new_user
):
    create_new_user.is_active = True
    create_new_user.save()

    kwargs = {
        "user_activation_uuid": create_new_user.user_activation_uuid
    }
    return kwargs
