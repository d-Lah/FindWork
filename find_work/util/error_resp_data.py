from rest_framework import status

auth_headers = "Authentication credentials were not provided."
user_with_given_email_not_found = "User with given email not found."
field_empty = {
    "field_blank": "This field may not be blank.",
    "field_required": "This field is required."
}
user_not_found = "User not found."
invalid_email = "Enter a valid email address."
field_not_unique = "This field must be unique."
field_not_boolean = "Must be a valid boolean."
field_is_blank = "This field may not be blank."
field_is_required = "This field is required."
invalid_file_ext = "Invalid file extension."
file_size_too_large = "File size to large."
file_not_submitted = "No file was submitted."
reset_password_totp_incap = "Reset password TOTP is incapacitated."
totp_incap = "TOTP incapacitated."
already_enable = "Two-factor authentication is already enabled."
already_disable = "Two-factor authentication is already disabled."
user_activation_uuid_incap = "User activate uuid is incapacitated."
wrong_password = "Wrong password."


class AuthHeadersError:
    def get_status(self):
        return status.HTTP_401_UNAUTHORIZED

    def get_data(self):
        return {"detail": "Authentication credentials were not provided."}


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
    detail = {
        "opt1": "blank",
        "opt2": "required"
    }

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
        return {"fields": "Fields not found"}


class SpecializationNotFoundError:
    detail = "Specialization not found"

    def get_status(self):
        return status.HTTP_404_NOT_FOUND

    def get_data(self):
        return {"specialization": "Specialization not found"}


class SkillNotFoundError:
    detail = "Skill not found"

    def get_status(self):
        return status.HTTP_404_NOT_FOUND

    def get_data(self):
        return {"skill": "Skill not found"}


class WorkExperienceNotFoundError:
    detail = "Work experience not found"

    def get_status(self):
        return status.HTTP_404_NOT_FOUND

    def get_data(self):
        return {"work_experience": "Work experience not found"}


class TypeOfEmploymentNotFoundError:
    detail = "Type of employment not found"

    def get_status(self):
        return status.HTTP_404_NOT_FOUND

    def get_data(self):
        return {"type_of_employment": "Type of employment not found"}


class UserNotFoundError:
    def get_status(self):
        return status.HTTP_404_NOT_FOUND

    def get_data(self):
        return {"user": "User not found"}


class UserActivateUUIDIncapError:
    def get_status(self):
        return status.HTTP_409_CONFLICT

    def get_data(self):
        return {"user_activate_uuid": "User activate uuid is incapacitated"}


class TwoFactorAuthAlreadyEnabledError:
    def get_status(self):
        return status.HTTP_409_CONFLICT

    def get_data(self):
        return {"user": "Two-factor authentication is already enabled"}


class TwoFactorAuthAlreadyDisabledError:
    def get_status(self):
        return status.HTTP_409_CONFLICT

    def get_data(self):
        return {"user": "Two-factor authentication is already disabled"}


class InvalidFileExtError:
    def get_status(self):
        return status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    def get_data(self):
        return {"file": "Invalid file extension"}


class FileSizeTooLargeError:
    def get_status(self):
        return status.HTTP_413_REQUEST_ENTITY_TOO_LARGE

    def get_data(self):
        return {"file": "File size to large"}


class WrongPasswordError:
    def get_status(self):
        return status.HTTP_403_FORBIDDEN

    def get_data(self):
        return {"password": "Wrong passwor"}


class WrongTOTPTokenError:
    def get_status(self):
        return status.HTTP_403_FORBIDDEN

    def get_data(self):
        return {"totp_token": "Wrong totp token"}


class ResumeNotFoundError:
    def get_status(self):
        return status.HTTP_404_NOT_FOUND

    def get_data(self):
        return {"resume": "Resume not found"}


class ForbiddenRequestDataError:
    def get_status(self):
        return status.HTTP_403_FORBIDDEN


class UserNotEmployerError:
    def get_status(self):
        return status.HTTP_403_FORBIDDEN

    def get_data(self):
        return {"detail": "User not employer"}


class UserNotEmployeeError:
    def get_status(self):
        return status.HTTP_403_FORBIDDEN

    def get_data(self):
        return {"detail": "User not employee"}


class NameAlreadyExistsError:
    def get_status(self):
        return status.HTTP_409_CONFLICT

    def get_data(self):
        return {"name": "Name already exists"}


class CompanyNotFoundError:
    def get_status(self):
        return status.HTTP_404_NOT_FOUND

    def get_data(self):
        return {"company": "Company not found"}


class UserNotCompanyOwner:
    def get_status(self):
        return status.HTTP_403_FORBIDDEN

    def get_data(self):
        return {"detail": "User not company owner"}


class VacancyNotFound:
    detail = "Vacancy not found"

    def get_status(self):
        return status.HTTP_404_NOT_FOUND

    def get_data(self):
        return {"vacancy": "Vacancy not found"}


class CompanyNotVacancyCreator:
    def get_status(self):
        return status.HTTP_403_FORBIDDEN

    def get_data(self):
        return {"detail": "Company not vacancy creator"}
