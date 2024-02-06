import pytest

from find_work.settings import BASE_DIR


@pytest.fixture()
def data_to_upload_company_avatar():
    data = {
        "company_avatar_url": (
            BASE_DIR / "media" / "for_test" / "upload_user_avatar.png"
        ).open("rb")
    }
    return data


@pytest.fixture()
def data_to_upload_company_avatar_w_big_file():
    data = {
        "company_avatar_url": (
            BASE_DIR / "media" / "for_test" / "img_size_too_large.png"
        ).open("rb")
    }
    return data


@pytest.fixture()
def data_to_upload_company_avatar_w_file_w_invalid_ext():
    data = {
        "company_avatar_url": (
            BASE_DIR / "media" / "for_test" / "invalid_img_ext.gif"
        ).open("rb")
    }
    return data
