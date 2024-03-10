from rest_framework import permissions

from company.models import Company


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
