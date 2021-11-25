from rest_framework import permissions


class IsPhotoAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or view.action in ['like', 'dislike', 'comment']:
            return True
        return obj.author == request.user


class IsCommentAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user_is_author = obj.author == request.user
        if view.action == 'destroy':
            return user_is_author | request.user.groups.filter(name='moderator').exists()
        return user_is_author
