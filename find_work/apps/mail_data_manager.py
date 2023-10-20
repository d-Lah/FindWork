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


class MailMessage(ABC):
    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def get_mail_message(self):
        pass


class MailMessageInRegisterNewUser(MailMessage):
    def __init__(self, user_first_name, link):
        super().__init__()
        self.user_first_name = user_first_name
        self.link = link

    def get_mail_message(self):
        message = f"Activate you account {self.link}"
        return message
