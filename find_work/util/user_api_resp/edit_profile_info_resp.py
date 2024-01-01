from rest_framework import status
from rest_framework.response import Response


class EditProfileInfoResp:
    resp_data = {
        "errors": [
            {"error": "Fields cannot be empty"},
        ],
        "successes": [
            {"success": "Update user profile info"}
        ]
    }

    def resp_fields_empty_error(self):
        return Response(
            self.resp_data["errors"][0],
            status=status.HTTP_400_BAD_REQUEST
        )

    def resp_update(self):
        return Response(
            self.resp_data["successes"][0],
            status=status.HTTP_200_OK
        )
