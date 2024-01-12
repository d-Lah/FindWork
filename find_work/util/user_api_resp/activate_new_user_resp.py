from rest_framework import status
from rest_framework.response import Response


class ActivateNewUserResp:
    resp_data = {
        "errors": [
            {"error": "User already activated"}
        ],
        "successes": [
            {"success": "Activate two factor auth"}
        ]
    }

    def resp_user_already_activated_error(self):
        return Response(
            self.resp_data["errors"][0],
            status=status.HTTP_409_CONFLICT
        )

    def resp_update(self):
        return Response(
            self.resp_data["successes"][0],
            status=status.HTTP_200_OK
        )
