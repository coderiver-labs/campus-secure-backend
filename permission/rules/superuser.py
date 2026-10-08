from permission.core.base import BasePermissionWithBypass

class SuperuserProtectionPermission(BasePermissionWithBypass):
    
    def check_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            return True

        if getattr(obj, "is_superuser", False):
            return False
        return True
