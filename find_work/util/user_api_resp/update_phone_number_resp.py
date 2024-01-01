from rest_framework import status
from rest_framework.response import Response


class UpdatePhoneNumberResp:
    resp_data = {
        "errors": [
            {"error": "Fields cannot be empty"},
            {"error": "Phone number already exist"}
        ],
        "successes": [
            {"success": "User phone number has update"}
        ]
    }

    def resp_fields_empty_error(self):
        return Response(
            self.resp_data["errors"][0],
            status=status.HTTP_400_BAD_REQUEST
        )

    def resp_phone_number_already_exists_error(self):
        return Response(
            self.resp_data["errors"][1],
            status=status.HTTP_409_CONFLICT
        )

    def resp_update(self):
        return Response(
            self.resp_data["successes"][0],
            status=status.HTTP_200_OK
        )
