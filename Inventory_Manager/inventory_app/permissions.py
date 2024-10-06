from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

# Custom permission to allow only the owner of an object or an admin to edit or delete it.
class IsOwnerOrReadOnly(permissions.BasePermission):

    message = 'You must be the owner or Admin of this object to Modify this Item.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user and request.user.is_staff:
            return True
        
        if obj.owner == request.user:
            return True
        
        # Allow access if the user is the owner
        return obj.owner == request.user
        
        # raise PermissionDenied(detail=self.message)
    
        

# Custom permission to allow only admin users to create, update, or delete objects.
class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'You must be an Admin to perform this action.'

    def has_permission(self, request, view):
        # Allow read-only access for safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_staff and request.user:
            return True
        
        # Allow full access if the user is an admin
        return request.user and request.user.is_staff
        
       # raise PermissionDenied(detail=self.message)