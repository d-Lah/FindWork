import pytest

from find_work.settings import BASE_DIR


@pytest.fixture()
def data_to_upload_avatar():
    data = {
        "user_avatar_url": (
            BASE_DIR / "media" / "for_test" / "upload_user_avatar.png"
        ).open("rb")
    }
    return data


@pytest.fixture()
def data_to_upload_avatar_wo_image():
    data = {
        "user_avatar_url": ""
    }
    return data


@pytest.fixture()
def data_to_upload_avatar_w_big_file():
    data = {
        "user_avatar_url": (
            BASE_DIR / "media" / "for_test" / "img_size_too_large.png"
        ).open("rb")
    }
    return data


@pytest.fixture()
def data_to_upload_avatar_w_file_w_invalid_ext():
    data = {
        "user_avatar_url": (
            BASE_DIR / "media" / "for_test" / "invalid_img_ext.gif"
        ).open("rb")
    }
    return data
