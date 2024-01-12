from rest_framework import status
from rest_framework.response import Response


class ValidateTOTPTokenResp:
    resp_data = {
        "errors": [
            {"error": "Fields cannot be empty"},
            {"error": "Wrong TOTP token"},
        ],
        "successes": [
            {"success": "TOTP token is valid"}
        ]
    }

    def resp_fields_empty_error(self):

        return Response(
            self.resp_data["errors"][0],
            status=status.HTTP_400_BAD_REQUEST
        )

    def resp_wrong_totp_token_error(self):
        return Response(
            self.resp_data["errors"][1],
            status=status.HTTP_403_FORBIDDEN
        )

    def resp_valid(self):
        return Response(
            self.resp_data["successes"][0],
            status=status.HTTP_200_OK
        )
