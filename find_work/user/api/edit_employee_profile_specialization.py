from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import (
    EmployeeProfile,
    EmployeeSpecialization
)
from user.serializer import EditEmployeeProfileSpecializationSerializer

from util.user_api_resp.edit_employee_profile_specialization_resp import (
    EditEmployeeProfileSpecializationResp
)


class EditEmployeeProfileSpecialization(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        serializer = EditEmployeeProfileSpecializationSerializer(
            data=request.data
        )

        serializer.is_valid()
        if serializer.errors:
            return EditEmployeeProfileSpecializationResp(
            ).resp_fields_empty_error()

        user_id = request.user.id

        employee_profile = EmployeeProfile.objects.filter(
            profile__user__id=user_id
        ).first()

        serializer_data = serializer.validated_data

        specializations_list = []

        for id in serializer_data["id"]:
            employee_specialization = EmployeeSpecialization.objects.filter(
                pk=id
            ).first()

            if not employee_specialization:
                return EditEmployeeProfileSpecializationResp(
                ).resp_specialization_not_found_error()

            specializations_list.append(employee_specialization)

        for specialization in specializations_list:
            employee_profile.specialization.add(specialization)

        return EditEmployeeProfileSpecializationResp().resp_update()
