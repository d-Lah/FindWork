from rest_framework import status

create = {
    "status_code": status.HTTP_201_CREATED,
    "data": {"detail": "Create."}
}

upload = {
    "status_code": status.HTTP_201_CREATED,
    "data": {"detail": "Upload."}
}

update = {
    "status_code": status.HTTP_200_OK,
    "data": {"detail": "Update."}
}

get = {
    "status_code": status.HTTP_200_OK,
    "data": {"detail": "Get."}
}

validate = {
    "status_code": status.HTTP_200_OK,
    "data": {"detail": "Validate."}
}

delete = {
    "status_code": status.HTTP_200_OK,
    "data": {"detail": "Delete."}
}


class CreateSuccess:
    status_code = status.HTTP_201_CREATED
    detail = {"detail": "Create."}

    def get_status(self):
        return status.HTTP_201_CREATED

    def get_data(self):
        return {"success": "Create"}


class UpdateSuccess:
    status_code = status.HTTP_200_OK
    detail = {"detail": "Update."}

    def get_status(self):
        return status.HTTP_200_OK

    def get_data(self):
        return {"success": "Update"}


class UploadSuccess:
    status_code = status.HTTP_201_CREATED
    detail = {"detail": "Upload."}

    def get_status(self):
        return status.HTTP_201_CREATED

    def get_data(self):
        return {"success": "Upload"}


class GetSuccess:
    # NOTE: uncomment this, when will be on vacancy editing

    status_code = status.HTTP_200_OK

    def __init__(self, data=None):
        self.detail = {
            "detail": "Get.",
            "data": data
        }

    def get_status(self):
        return status.HTTP_200_OK

    def get_data(self, data=None):
        return {
            "success": "Get",
            "data": data
        }


class ValidateSuccess:
    status_code = status.HTTP_200_OK
    detail = {"detail": "Validate"}

    def get_status(self):
        return status.HTTP_200_OK

    def get_data(self):
        return {"success": "Validate"}


class DeleteSuccess:
    status_code = status.HTTP_200_OK
    detail = {"detail": "Delete"}

    def get_status(self):
        return status.HTTP_200_OK

    def get_data(self):
        return {"success": "Delete"}
