from user.models import User
from find_work.settings import (
    ALLOWED_IMAGE_EXT,
    IMAGE_MAX_MEMORY_SIZE
)
from apps.object_exception import (
    InvalidImageExtError,
    ImageSizeToLargeError,
    EmailAlreadyExistsError,
    PhoneNuberAlreadyExistsError,
)


class ValidateEmailAndPhoneNumberOnExists:
    def __init__(
            self,
            email,
            phone_number,
    ):
        self.email = email
        self.phone_number = phone_number

    def is_email_exists(self):
        email_to_validate_exists = self.email
        _is_email_exists = User.objects.filter(
            email=email_to_validate_exists
        ).exists()
        if _is_email_exists:
            raise EmailAlreadyExistsError()

    def is_phone_number_exists(self):
        phone_number_to_validate_exists = self.phone_number
        _is_phone_number_exists = User.objects.filter(
            phone_number=phone_number_to_validate_exists
        ).exists()
        if _is_phone_number_exists:
            raise PhoneNuberAlreadyExistsError()


class ValidateImageSizeAndExt:
    def __init__(
            self,
            image
    ):
        self.image = image

    def is_image_size_too_large(self):
        if self.image.size > IMAGE_MAX_MEMORY_SIZE:
            raise ImageSizeToLargeError()

    def is_valid_image_ext(self):
        image_ext = self.image.name.split(".")[1]
        if image_ext not in ALLOWED_IMAGE_EXT:
            raise InvalidImageExtError()
