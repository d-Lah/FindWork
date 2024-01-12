from rest_framework import status
from rest_framework.response import Response


class UploadAvatarResp:
    resp_data = {
        "errors": [
            {"error": "Fields cannot be empty"},
            {"error": "File size to large"},
            {"error": "Invalid file extension"}
        ],
        "successes": [
            {"success": "User avatar has upload"}
        ]
    }

    def resp_fields_empty_error(self):
        return Response(
            self.resp_data["errors"][0],
            status=status.HTTP_400_BAD_REQUEST
        )

    def resp_file_size_to_large_error(self):

        return Response(
            self.resp_data["errors"][1],
            status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        )

    def resp_invalid_file_ext_error(self):
        return Response(
            self.resp_data["errors"][2],
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )

    def resp_upload(self):
        return Response(
            self.resp_data["successes"][0],
            status=status.HTTP_201_CREATED
        )
