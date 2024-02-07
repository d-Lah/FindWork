from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from find_work.settings import HTTP_LOCALHOST

from user.models import User
from user.serializer import UpdatePasswordSerializer

from util.mail_data_manager import (
    MailSubjectInUpdateUserPassword,
    MailMessageInUpdateUserPassword,
)
from util.mail_sender import MailSender
from util.success_resp_data import UpdateSuccess
from util.error_resp_data import FieldsEmptyError


class UpdatePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        serializer = UpdatePasswordSerializer(data=request.data)
        serializer.is_valid()

        deserialized_data = serializer.validated_data

        if serializer.errors:
            return Response(
                status=FieldsEmptyError().get_status(),
                data=FieldsEmptyError().get_data()
            )

        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        user.password = make_password(deserialized_data["password"])
        user.save()

        link_on_generate_reset_password_uuid = (
            HTTP_LOCALHOST
            + reverse("user_api:generate_reset_password_totp")
        )
        mail_subject = MailSubjectInUpdateUserPassword().get_mail_subject()
        mail_message = MailMessageInUpdateUserPassword(
            link_on_generate_reset_password_uuid
        ).get_mail_message()

        MailSender(
            mail_subject=mail_subject,
            mail_message=mail_message,
            for_user=user.email
        ).send_mail_to_user()

        return Response(
            status=UpdateSuccess().get_status(),
            data=UpdateSuccess().get_data()
        )
