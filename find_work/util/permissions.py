from rest_framework import permissions

from user.models import User

from resume.models import Resume

from company.models import Company

from vacancy.models import Vacancy

from util import error_resp_data
from util.exceptions import NotFoundException


class IsEmployer(permissions.BasePermission):
    message = "User not employer"

    def has_permission(
            self,
            request,
            view
    ):
        return request.user.is_employer


class IsEmployee(permissions.BasePermission):
    message = "User not employee"

    def has_permission(
            self,
            request,
            view
    ):
        return request.user.is_employee


class IsVacancyFound(permissions.BasePermission):
    message = "Vacancy not found"

    def has_permission(
            self,
            request,
            view
    ):
        vacancy_id = view.kwargs["vacancy_id"]
        vacancy = Vacancy.objects.filter(
            pk=vacancy_id,
            is_delete=False
        )
        if not vacancy:
            raise NotFoundException(error_resp_data.VacancyNotFound.detail)

        return True


class IsResumeFound(permissions.BasePermission):
    message = "Resume not found"

    def has_permission(
            self,
            request,
            view
    ):
        resume_id = view.kwargs["resume_id"]
        resume = Resume.objects.filter(
            pk=resume_id,
            is_delete=False
        )
        if not resume:
            raise NotFoundException(error_resp_data.resume_not_found)

        return True


class IsCompanyFound(permissions.BasePermission):
    message = "Company not found"

    def has_permission(
            self,
            request,
            view
    ):
        company_id = view.kwargs["company_id"]
        company = Company.objects.filter(
            pk=company_id,
            is_delete=False
        )
        if not company:
            raise NotFoundException(error_resp_data.company_not_found)

        return True


class IsCompanyOwner(permissions.BasePermission):
    message = "User not company owner"

    def has_permission(
            self,
            request,
            view
    ):
        user_id = request.user.id

        company = Company.objects.filter(author__id=user_id).first()

        if not company:
            return False

        return True


class IsResumeOwner(permissions.BasePermission):
    message = "User not resume owner"

    def has_permission(
            self,
            request,
            view
    ):
        user_id = request.user.id

        resume = Resume.objects.filter(author__id=user_id).first()

        if not resume:
            return False

        return True


class IsVacancyCreator(permissions.BasePermission):
    message = "Company not vacancy creator"

    def has_permission(
            self,
            request,
            view
    ):
        company = request.user.company

        vacancy_id = view.kwargs["vacancy_id"]
        vacancy = Vacancy.objects.filter(
            pk=vacancy_id,
            company=company
        )

        if not vacancy:
            return False

        return True


class IsUserFound(permissions.BasePermission):
    message = "User not found."

    def has_permission(
            self,
            request,
            view
    ):
        user_id = view.kwargs["user_id"]
        user = User.objects.filter(
            pk=user_id,
        )
        if not user:
            raise NotFoundException(error_resp_data.user_not_found)

        return True
