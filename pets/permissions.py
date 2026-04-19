from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only for everyone
        if request.method in SAFE_METHODS:
            return True
        
        # Only admin can write
        return request.user and request.user.is_staff


class IsReviewAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read allowed
        if request.method in SAFE_METHODS:
            return True
        
        # Only review author can edit/delete
        return obj.user == request.user