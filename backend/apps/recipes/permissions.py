from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Read for all; write for auth; only owner (or staff) can edit.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        
        owner = getattr(obj, 'user', None) or getattr(obj, 'owner', None)
        return owner and owner == request.user
    
class IsStaffOrManager(permissions.BasePermission):
    """
    Write only for staff or users in 'manager' group; read for everyone
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        u = request.user
        return u and u.is_authenticated and (u.is_staff or u.groups.filter(name='manager').exists())

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        recipe = getattr(obj, 'recipe', None)
        return recipe and recipe.user == request.user
    
class IsRecipeOwnerForChildren(permissions.BasePermission):
    """
    For Ingredient/Instruction: read for all; modifying allowed only if the
    parent recipe belongs to the user (or staff).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        recipe = getattr(obj, 'recipe', None)
        return recipe and recipe.user == request.user