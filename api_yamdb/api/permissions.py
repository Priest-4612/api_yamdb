from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrMod(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return (obj.author == request.user or request.user.is_admin
                or request.user.is_moderator)
