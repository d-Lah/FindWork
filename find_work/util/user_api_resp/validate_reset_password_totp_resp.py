from rest_framework import status
from rest_framework.response import Response


class ValidateResetPasswordTOTPResp:
    resp_data = {
        "errors": [
            {"error": "Fields cannot be empty"},
            {"error": "Invalid email address"},
            {"error": "User with given credentials not found"},
            {"error": "Reset password totp is incapacitate"},
        ],
        "successes": [
            {"success": "Reset password totp is valid"}
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
            status=status.HTTP_400_BAD_REQUEST
        )

    def resp_user_not_found_error(self):
        return Response(
            self.resp_data["errors"][2],
            status=status.HTTP_404_NOT_FOUND
        )

    def resp_reset_password_totp_incap_error(self):
        return Response(
            self.resp_data["errors"][3],
            status=status.HTTP_403_FORBIDDEN
        )

    def resp_valid(self):
        return Response(
            self.resp_data["successes"][0],
            status=status.HTTP_200_OK
        )
