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


class AdminOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        methods = ['retrieve', 'update', 'partial_update', 'destroy']
        return (
            request.user.role == 'admin' or view.action in methods
        )


class OwnerOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        methods = ['retrieve', 'update', 'partial_update']
        return (
            request.user.is_authenticated
            and obj.username == request.user
            and view.action in methods
        )
