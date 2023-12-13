import pytest

from find_work.settings import BASE_DIR


@pytest.fixture()
def data_to_upload_user_avatar():
    data = {
        "user_avatar_url": (
            BASE_DIR / "media" / "for_test" / "upload_user_avatar.png"
        ).open("rb")
    }
    return data


@pytest.fixture()
def data_to_response_image_size_too_large_error():
    data = {
        "user_avatar_url": (
            BASE_DIR / "media" / "for_test" / "img_size_too_large.png"
        ).open("rb")
    }
    return data


@pytest.fixture()
def data_to_resonse_invalid_image_ext_error():
    data = {
        "user_avatar_url": (
            BASE_DIR / "media" / "for_test" / "invalid_img_ext.gif"
        ).open("rb")
    }
    return data
