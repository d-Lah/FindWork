from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from find_work.permissions import IsEmployer

from company.models import Company
from company.serializer import EditCompanyInfoSerializer

from util.error_resp_data import (
    FieldsEmptyError,
    CompanyNotFoundError,
    NameAlreadyExistsError,
)
from util.success_resp_data import (
    UpdateSuccess
)


def is_fields_empty(errors):
    if not errors:
        return False

    for field in errors:
        if "blank" in errors[field][0]:
            return True
    return False


def is_name_already_exists(errors):
    if not errors.get("name"):
        return False

    if errors["name"][0] == "company with this name already exists.":
        return True

    return False


class EditCompanyInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    def put(
            self,
            request,
    ):
        serializer = EditCompanyInfoSerializer(data=request.data)

        serializer.is_valid()

        if is_fields_empty(serializer.errors):
            return Response(
                status=FieldsEmptyError().get_status(),
                data=FieldsEmptyError().get_data()
            )

        if is_name_already_exists(serializer.errors):
            return Response(
                status=NameAlreadyExistsError().get_status(),
                data=NameAlreadyExistsError().get_data()
            )

        user_id = request.user.id
        company = Company.objects.filter(
            author__id=user_id,
            is_delete=False
        ).first()

        if not company:
            return Response(
                status=CompanyNotFoundError().get_status(),
                data=CompanyNotFoundError().get_data()
            )

        serializer_data = serializer.validated_data

        company.name = serializer_data["name"]
        company.save()

        return Response(
            status=UpdateSuccess().get_status(),
            data=UpdateSuccess().get_data()
        )
