from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from company.models import (
    Company,
    CompanyAvatar
)
from company.serializer import UploadCompanyAvatarSerializer

from util.error_resp_data import (
    FieldsEmptyError,
    InvalidFileExtError,
    FileSizeTooLargeError,
)
from util.error_exceptions import (
    IsFileFieldsEmpty,
    IsFileFieldsInvalid,
    IsFileFieldsSizeTooLarge
)
from util.permissions import IsEmployer
from util.success_resp_data import UploadSuccess
from util.error_validation import ErrorValidation


class UploadCompanyAvatar(APIView):

    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    def post(
            self,
            request
    ):
        serializer = UploadCompanyAvatarSerializer(data=request.FILES)

        serializer.is_valid()

        error_validation = ErrorValidation(serializer.errors)
        try:
            error_validation.is_file_fields_empty()
            error_validation.is_file_fields_invalid()
            error_validation.is_file_fields_size_too_large()
        except IsFileFieldsEmpty:
            return Response(
                status=FieldsEmptyError().get_status(),
                data=FieldsEmptyError().get_data()
            )
        except IsFileFieldsInvalid:
            return Response(
                status=InvalidFileExtError().get_status(),
                data=InvalidFileExtError().get_data()
            )
        except IsFileFieldsSizeTooLarge:
            return Response(
                status=FileSizeTooLargeError().get_status(),
                data=FileSizeTooLargeError().get_data()
            )

        serializer_data = serializer.validated_data

        user_id = request.user.id
        company = Company.objects.filter(author__id=user_id).first()

        new_company_avatar = CompanyAvatar.objects.create(
            for_company=company,
            company_avatar_url=serializer_data["company_avatar_url"]
        )

        company.user_avatar = new_company_avatar
        company.save()

        return Response(
            status=UploadSuccess().get_status(),
            data=UploadSuccess().get_data()
        )
