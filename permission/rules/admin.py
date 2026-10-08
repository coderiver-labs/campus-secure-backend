from rest_framework.permissions import BasePermission
from permission.core.base import BasePermissionWithBypass

class AdminSelfProtectionPermission(BasePermissionWithBypass):

    def check_object_permission(self, request, view, obj):
        user = request.user

        if user.role == "admin":
            if obj.uuid == user.uuid and view.action == "destroy":
                return False
        return True
    
