from permission.core.base import BasePermissionWithBypass


# create API base permission

class UserDomainPermission(BasePermissionWithBypass):

    def check_object_permission(self, request, view, obj):
        user = request.user
        
        if user.uuid == obj.uuid:
            return True
        
        if obj.role in ["student", "teacher"]:
            return True

        return False