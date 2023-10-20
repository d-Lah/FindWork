from user.models import User
from apps.object_exception import (
    EmailAlreadyExistsError,
    PhoneNuberAlreadyExistsError
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
