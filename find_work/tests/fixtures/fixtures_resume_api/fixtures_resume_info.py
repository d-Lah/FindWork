import pytest


@pytest.fixture()
def data_to_resume_info_w_resume_id(create_resume):
    kwargs = {
        "resume_id": create_resume.pk
    }
    return kwargs


@pytest.fixture()
def data_to_resume_info_w_wrong_resume_id():
    kwargs = {
        "resume_id": 0
    }
    return kwargs
