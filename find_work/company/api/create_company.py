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
from util.error_exceptions import (
    IsFieldsEmpty,
    IsFieldsAlreadyExists
)
from util.success_resp_data import CreateSuccess
from util.error_validation import ErrorValidation


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

        error_validation = ErrorValidation(serializer.errors)
        try:
            error_validation.is_fields_empty()
            error_validation.is_fields_already_exists()
        except IsFieldsEmpty:
            return Response(
                status=FieldsEmptyError().get_status(),
                data=FieldsEmptyError().get_data()
            )
        except IsFieldsAlreadyExists:
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
