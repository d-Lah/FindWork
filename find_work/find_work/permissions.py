from rest_framework import permissions


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
