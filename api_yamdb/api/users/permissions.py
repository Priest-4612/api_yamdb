from rest_framework import permissions


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        methods = ['retrieve', 'update', 'partial_update', 'destroy']
        return (
            request.user.role == 'admin' or view.action in methods
        )


class OwnerOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        methods = ['retrieve', 'update', 'partial_update']
        return (
            request.user.is_authenticated
            and obj.username == request.user
            and view.action in methods
        )
