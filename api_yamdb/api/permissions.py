from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrMod(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                (request.method in SAFE_METHODS)
                or request.user.is_superuser
                or (request.user.role in ['user', 'admin', 'moderator'])
            )
        else:
            return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.is_superuser
                or (request.user.role in ['admin', 'moderator'])
                or obj.author == request.user
            )
        else:
            return request.method in SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.method in SAFE_METHODS
                or request.user.is_superuser
                or request.user.role == 'admin'
            )
        else:
            return request.method in SAFE_METHODS
