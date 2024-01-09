from rest_framework import status
from rest_framework.response import Response


class EditEmployeeProfileSpecializationResp:
    resp_data = {
        "errors": [
            {"error": "Fields cannot be empty"},
            {"error": "Specialization not found"}
        ],
        "successes": [
            {"success": "Update user employee profile info"}
        ]
    }

    def resp_fields_empty_error(self):
        return Response(
            self.resp_data["errors"][0],
            status=status.HTTP_400_BAD_REQUEST
        )

    def resp_specialization_not_found_error(self):
        return Response(
            self.resp_data["errors"][1],
            status=status.HTTP_404_NOT_FOUND
        )

    def resp_update(self):
        return Response(
            self.resp_data["successes"][0],
            status=status.HTTP_200_OK
        )
