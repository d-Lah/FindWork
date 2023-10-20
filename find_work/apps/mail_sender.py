from django.core.mail import send_mail

from find_work.settings import DEFAULT_FROM_EMAIL


class MailSender:
    def __init__(
            self,
            mail_subject,
            mail_message,
            for_user
    ):
        self.mail_subject = mail_subject
        self.mail_message = mail_message
        self.for_user = for_user

    def send_mail_to_user(self):
        send_mail(
            subject=self.mail_subject,
            message=self.mail_message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[self.for_user],
            fail_silently=False
        )
