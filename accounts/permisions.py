from rest_framework.permissions import BasePermission

class IsRegistration(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "registration"


class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"


class IsJudge(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "judge"


class IsCertification(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "certification"
