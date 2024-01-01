from rest_framework import status
from rest_framework.response import Response


class UpdateEmailResp:
    resp_data = {
        "errors": [
            {"error": "Fields cannot be empty"},
            {"error": "Invalid email address"},
            {"error": "Email already exist"},
        ],
        "successes": [
            {"success": "User email has update"}
        ]
    }

    def resp_fields_empty_error(self):
        return Response(
            self.resp_data["errors"][0],
            status=status.HTTP_400_BAD_REQUEST
        )

    def resp_invalid_email_address_error(self):
        return Response(
            self.resp_data["errors"][1],
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    def resp_email_already_exists_error(self):
        return Response(
            self.resp_data["errors"][2],
            status=status.HTTP_409_CONFLICT
        )

    def resp_update(self):
        return Response(
            self.resp_data["successes"][0],
            status=status.HTTP_200_OK
        )
