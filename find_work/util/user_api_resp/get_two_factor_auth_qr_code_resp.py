from rest_framework import status
from rest_framework.response import Response


class GetTwoFacteorAuthQRCodeResp:
    resp_data = {
        "successes": [
            {"success": "Get otp auth url"}
        ],
    }

    def resp_get(self, data):
        self.resp_data["successes"][0]["otp_auth_url"] = data

        return Response(
            self.resp_data["successes"][0],
            status=status.HTTP_200_OK
        )
