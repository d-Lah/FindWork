from util.error_resp_data import (
    InvalidFileExtError,
    FileSizeTooLargeError,
)
from util.error_exceptions import (
    IsFieldsEmpty,
    IsFieldsInvalid,
    IsFieldsNotFound,
    IsFileFieldsEmpty,
    IsFileFieldsInvalid,
    IsFieldsAlreadyExists,
    IsFileFieldsSizeTooLarge,
)


class ErrorValidation:
    def __init__(self, errors):
        self.errors = errors

    def is_fields_empty(self):
        for field in self.errors:
            if "blank" in self.errors[field][0]:
                raise IsFieldsEmpty

    def is_fields_already_exists(self):
        for field in self.errors:
            if "unique" in self.errors[field][0] or \
                    "exists" in self.errors[field][0]:
                raise IsFieldsAlreadyExists

    def is_fields_not_found(self):
        for field in self.errors:
            if "not found" in self.errors[field][0]:
                raise IsFieldsNotFound

    def is_fields_invalid(self):
        for field in self.errors:
            if "valid" in self.errors[field][0]:
                raise IsFieldsInvalid

    def is_file_fields_empty(self):
        for field in self.errors:
            if self.errors[field][0] == "No file was submitted.":
                raise IsFileFieldsEmpty

    def is_file_fields_size_too_large(self):
        error = FileSizeTooLargeError().get_data()["file"]
        for field in self.errors:
            if self.errors[field][0] == error:
                raise IsFileFieldsSizeTooLarge

    def is_file_fields_invalid(self):
        error = InvalidFileExtError().get_data()["file"]
        for field in self.errors:
            if self.errors[field][0] == error:
                raise IsFileFieldsInvalid
