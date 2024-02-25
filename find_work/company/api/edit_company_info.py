from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from company.models import Company
from company.serializer import EditCompanyInfoSerializer

from util.error_resp_data import (
    FieldsEmptyError,
    CompanyNotFoundError,
    NameAlreadyExistsError,
)
from util.error_exceptions import (
    IsFieldsEmpty,
    IsFieldsAlreadyExists
)
from util.permissions import IsEmployer
from util.success_resp_data import UpdateSuccess
from util.error_validation import ErrorValidation


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
