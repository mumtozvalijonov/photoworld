from rest_framework import permissions


class AccountPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.method in permissions.SAFE_METHODS or view.action in ['create', 'follow', 'unfollow']
