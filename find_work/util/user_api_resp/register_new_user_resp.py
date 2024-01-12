from rest_framework import status
from rest_framework.response import Response


class RegisterNewUserResp:
    resp_data = {
        "errors": [
            {"error": "Fields cannot be empty"},
            {"error": "Invalid email address"},
            {"error": []}
        ],
        "successes": [
            {"success": "User account has create"}
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

    def resp_fields_already_exists_error(self, data):
        if data.get("email"):
            self.resp_data["errors"][2]["error"].append(
                "Email already exist"
            )

        if data.get("phone_number"):
            self.resp_data["errors"][2]["error"].append(
                "Phone number already exist"
            )

        return Response(
            self.resp_data["errors"][2],
            status=status.HTTP_409_CONFLICT
        )

    def resp_create(self):
        return Response(
            self.resp_data["successes"][0],
            status=status.HTTP_201_CREATED
        )
