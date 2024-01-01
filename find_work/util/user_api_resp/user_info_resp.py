from rest_framework import status
from rest_framework.response import Response


class UserInfoResp:
    resp_data = {
        "successes": [
            {"success": "Get user info"}
        ],
    }

    def resp_get(self, data):
        self.resp_data["successes"][0].update(data)

        return Response(
            self.resp_data["successes"][0],
            status=status.HTTP_200_OK
        )
