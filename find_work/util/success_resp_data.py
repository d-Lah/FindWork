from rest_framework import status


class CreateSuccess:
    def get_status(self):
        return status.HTTP_201_CREATED

    def get_data(self):
        return {"success": "Create"}


class UpdateSuccess:
    def get_status(self):
        return status.HTTP_200_OK

    def get_data(self):
        return {"success": "Update"}


class UploadSuccess:
    def get_status(self):
        return status.HTTP_201_CREATED

    def get_data(self):
        return {"success": "Upload"}


class GetSuccess:
    def get_status(self):
        return status.HTTP_200_OK

    def get_data(self, data=None):
        return {
            "success": "Get",
            "data": data
        }


class ValidateSuccess:
    def get_status(self):
        return status.HTTP_200_OK

    def get_data(self):
        return {"success": "Validate"}


class DeleteSuccess:
    def get_status(self):
        return status.HTTP_200_OK

    def get_data(self):
        return {"success": "Delete"}
