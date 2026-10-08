

from rest_framework.permissions import BasePermission
# import decorators
from permission.core.decorators import superuser_bypass


# create base permission

class BasePermissionWithBypass(BasePermission):
    
    @superuser_bypass
    def has_permission(self, request, view):
        return self.check_permission(request=request, view=view)
    
    @superuser_bypass
    def has_object_permission(self, request, view, obj):
        return self.check_object_permission(request=request, view=view, obj=obj)
    
    # default methods
    def check_permission(self, request, view):
        return True

    def check_object_permission(self, request, view, obj):
        return True
    