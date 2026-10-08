from rest_framework.request import HttpRequest
from rest_framework.permissions import BasePermission, SAFE_METHODS

# import models
from accounts.models import CustomUser

# import utils
from utils.permissions.services import check_staff_permission



# Create Base Permission Or Policy Hare

class BaseUserRelatedPermissionPolicy(BasePermission):
    def has_permission(self, request: HttpRequest, view):
        user: CustomUser = request.user
        if user.is_anonymous:
            return False
        if user.is_superuser:
            return True
        if user.role == "admin":
            return True

        if request.method == "GET":
            staff_position = ["manager", "principal"]
            if user.role == "staff":
                return check_staff_permission(user=user, positions=staff_position)
            
        if request.method in ["PUT", "PATCH"]:
            staff_position = ["registrar"]
            if user.role == "staff":
                return check_staff_permission(user=user, positions=staff_position)

        return False
    

    
    
### Only Admin Permission 
class BaseAdminOnlyPermissionPolicy(BasePermission):

    def has_permission(self, request: HttpRequest, view):
        user = request.user
        if user.is_anonymous:
            return False
        if user.is_superuser:
            return True
        if user.role in ["admin"]:
            return True
        return False