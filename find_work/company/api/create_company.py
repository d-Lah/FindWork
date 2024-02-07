from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from find_work.permissions import IsEmployer

from company.models import Company
from company.serializer import CreateCompanySerializer

from user.models import User

from util.error_resp_data import (
    FieldsEmptyError,
    NameAlreadyExistsError,
)
from util.success_resp_data import (
    CreateSuccess
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


class CreateCompany(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsEmployer,
    ]

    def post(
            self,
            request,
    ):
        serializer = CreateCompanySerializer(data=request.data)

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
        author = User.objects.filter(pk=user_id).first()

        serializer_data = serializer.validated_data

        Company.objects.create(
            name=serializer_data["name"],
            author=author
        )

        return Response(
            status=CreateSuccess().get_status(),
            data=CreateSuccess().get_data()
        )
