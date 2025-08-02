from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsManager(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.groups.filter(name='manager').exists()

class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.user == request.user
        return False
        