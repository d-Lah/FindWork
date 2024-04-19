from rest_framework import permissions

from user.models import User

from company.models import Company

from vacancy.models import Vacancy

from rest_framework import status

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
    status_code = status.HTTP_404_NOT_FOUND
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


class IsCompanyOwner(permissions.BasePermission):
    message = "User not company owner"

    def has_permission(
            self,
            request,
            view
    ):
        user_id = request.user.id

        company = Company.objects.filter(author__id=user_id).first()

        if company:
            return True
        else:
            return False


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

        if vacancy:
            return True
        else:
            return False


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
