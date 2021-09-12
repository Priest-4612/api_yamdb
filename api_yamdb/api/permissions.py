from rest_framework import permissions

from users.models import User


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or (request.user.is_authenticated and request.user.role == 'admin')
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser
            or (request.user.is_authenticated and request.user.role == 'admin')
            or view.action == 'retrieve'
        )
