from rest_framework import status


class AuthHeadersError:
    def get_status(self):
        return status.HTTP_401_UNAUTHORIZED


class InvalidEmailAdressError:
    def get_status(self):
        return status.HTTP_422_UNPROCESSABLE_ENTITY

    def get_data(self):
        return {"email": "Invalid email address"}


class EmailAlreadyExistsError:
    def get_status(self):
        return status.HTTP_409_CONFLICT

    def get_data(self):
        return {"email": "Email already exists"}


class FieldsEmptyError:
    def get_status(self):
        return status.HTTP_400_BAD_REQUEST

    def get_data(self):
        return {"fields": "Fields cannot be empty"}


class ResetPasswordTOTPIncapError:
    def get_status(self):
        return status.HTTP_403_FORBIDDEN

    def get_data(self):
        return {"reset_password_totp": "Reset password totp is incapacitated"}


class FieldsNotFoundError:
    def get_status(self):
        return status.HTTP_404_NOT_FOUND

    def get_data(self):
        return {
            "specialization": "Specialization not found",
            "skill": "Skill not found",
            "work_experience": "Work experience not found",
            "type_of_employment": "Type of employment not found",
        }


class UserNotFoundError:
    def get_status(self):
        return status.HTTP_404_NOT_FOUND

    def get_data(self):
        return {"user": "User not found"}


class UserActivateUUIDIncapError():
    def get_status(self):
        return status.HTTP_409_CONFLICT

    def get_data(self):
        return {"user_activate_uuid": "User activate uuid is incapacitated"}


class TwoFactorAuthAlreadyEnabledError():
    def get_status(self):
        return status.HTTP_409_CONFLICT

    def get_data(self):
        return {"user": "Two-factor authentication is already enabled"}


class TwoFactorAuthAlreadyDisabledError():
    def get_status(self):
        return status.HTTP_409_CONFLICT

    def get_data(self):
        return {"user": "Two-factor authentication is already disabled"}


class InvalidFileExtError():
    def get_status(self):
        return status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    def get_data(self):
        return {"file": "Invalid file extension"}


class FileSizeTooLargeError():
    def get_status(self):
        return status.HTTP_413_REQUEST_ENTITY_TOO_LARGE

    def get_data(self):
        return {"file": "File size to large"}


class WrongPasswordError():
    def get_status(self):
        return status.HTTP_403_FORBIDDEN

    def get_data(self):
        return {"password": "Wrong passwor"}


class WrongTOTPTokenError():
    def get_status(self):
        return status.HTTP_403_FORBIDDEN

    def get_data(self):
        return {"totp_token": "Wrong totp token"}


class ResumeNotFoundError():
    def get_status(self):
        return status.HTTP_404_NOT_FOUND

    def get_data(self):
        return {"resume": "Resume not found"}


class ForbiddenRequestDataError:
    def get_status(self):
        return status.HTTP_403_FORBIDDEN
