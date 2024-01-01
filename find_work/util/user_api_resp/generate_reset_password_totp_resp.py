from rest_framework import status
from rest_framework.response import Response


class GenerateResetPasswordTOTPResp:
    resp_data = {
        "errors": [
            {"error": "Fields cannot be empty"},
            {"error": "Invalid email address"},
            {"error": "User with given credentials not found"}
        ],
        "successes": [
            {"success": "Generate user reset password totp"}
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

    def resp_user_not_found_error(self):
        return Response(
            self.resp_data["errors"][2],
            status=status.HTTP_404_NOT_FOUND
        )

    def resp_create(self):
        return Response(
            self.resp_data["successes"][0],
            status=status.HTTP_201_CREATED
        )
