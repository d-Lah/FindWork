class EmailAlreadyExistsError(Exception):
    pass


class PhoneNuberAlreadyExistsError(Exception):
    pass


class ImageSizeToLargeError(Exception):
    pass


class InvalidImageExtError(Exception):
    pass


class EmailFieldEmptyError(Exception):
    pass


class PasswordFieldEmptyError(Exception):
    pass


class ResetPasswordPasswordTOTPFieldEmptyError(Exception):
    pass
