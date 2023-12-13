from abc import (
    ABC,
    abstractmethod
)


class MailSubject(ABC):
    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def get_mail_subject(self):
        pass


class MailSubjectInRegisterNewUser(MailSubject):
    def __init__(self):
        super().__init__()

    def get_mail_subject(self):
        subject = "Your account has create"
        return subject


class MailSubjectInUpdateUserPassword(MailSubject):
    def __init__(self):
        super().__init__()

    def get_mail_subject(self):
        subject = "Your password update"
        return subject


class MailSubjectInGenerateResetPasswordUuid(MailSubject):
    def __init__(self):
        super().__init__()

    def get_mail_subject(self):
        subject = "Reset password uuid"
        return subject


class MailMessage(ABC):
    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def get_mail_message(self):
        pass


class MailMessageInRegisterNewUser(MailMessage):
    def __init__(self, link):
        super().__init__()
        self.link = link

    def get_mail_message(self):
        message = f"Activate you account {self.link}"
        return message


class MailMessageInUpdateUserPassword(MailMessage):
    def __init__(self, link):
        super().__init__()
        self.link = link

    def get_mail_message(self):
        message = f"Your password has been update. If you don't change password {self.link}"
        return message


class MailMessageInGenerateResetPasswordUuid(MailMessage):
    def __init__(self, reset_password_uuid):
        super().__init__()
        self.reset_password_uuid = reset_password_uuid

    def get_mail_message(self):
        message = f"Here is your uuid: {self.reset_password_uuid}"
        return message
