
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only owner can delete shapes
    """
    def has_object_permission(self,request,view,obj):

        # View methods (GET HEAD OPTIONS) 
        allowed = request.method in permissions.SAFE_METHODS

        # Is owner or superuser
        allowed |= (obj.author == request.user) | request.user.is_staff

        return allowed

class IsStaffOrSelf(permissions.BasePermission):
    """
    Users can be viewed / modified by staff or themselves
    """

    def has_object_permission(self,request,view,obj):
        allowed = bool(request.user & obj == request.user)

        return allowed


