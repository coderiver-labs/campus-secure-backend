from django.db.models.query import QuerySet

# DRF
from rest_framework.request import Request
from rest_framework.request import HttpRequest
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_access_policy.access_policy import AccessPolicy

# import models
from accounts.models import CustomUser

# import utils
from utils.decorator.permissions import default_allow_admin_and_superuser
from utils.permissions.services import check_staff_permission

# import policy
from rest_access_policy.access_policy import AccessPolicy

# import base permission 
from accounts.permissions.base_policy import BaseAdminOnlyPermissionPolicy, BaseUserRelatedPermissionPolicy

# create policy hare



class TeacherAssignmentPolicy(AccessPolicy):

    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": ["authenticated",],
            "effect": "allow",
            "condition": ["can_list_retrieve_assignment"]
        },
        {
            "action": ["create", "update", "partial_update", "destroy"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["can_create_update_partial_update_destroy"]
        }
    ]

    @classmethod
    def scope_queryset(cls, request: Request, qs: QuerySet):
        user: CustomUser = request.user

        if user.is_superuser or user.role == "admin":
            return qs

        staff_position = ["manager", "principal"]
        if user.role == "staff":
            if check_staff_permission(user=user, positions=staff_position):
                return qs

        if user.role == "teacher":
            return qs.filter(teacher=user.teacher_profile)
        return qs.none()
        

    @default_allow_admin_and_superuser
    def can_list_retrieve_assignment(self, request: Request, view, action):
        user: CustomUser = request.user

        staff_position = ["manager", "principal"]
        if user.role == "staff":
            return check_staff_permission(user=user, positions=staff_position)

        if user.role == "teacher":
            return True
        
        return False


    @default_allow_admin_and_superuser
    def can_create_update_partial_update_destroy(self, request: Request, view, action):
        return False


    
class ProfileAPIViewPolicy(BasePermission):
    def has_permission(self, request: Request, view):
        user: CustomUser = request.user
        if user.is_anonymous:
            return False
        if user.is_superuser:
            return True
        
        if user.role in ["student", "teacher", "staff", "admin"]:
            return True
        return False
        


"""_________________Student Related Info__________________"""
class StudentRelatedInfoPolicy(BaseUserRelatedPermissionPolicy):
    def has_permission(self, request, view):
        return super().has_permission(request, view)

"""__________________Teacher Related Info__________________"""
class TeacherRelatedViewPolicy(BaseUserRelatedPermissionPolicy):
    def has_permission(self, request, view):
        return super().has_permission(request, view)


"""________________Staff Related Info__________________"""
# admin only view
class StaffPositionViewPolicy(BaseAdminOnlyPermissionPolicy):
    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
class StaffContactInfoViewPolicy(BaseUserRelatedPermissionPolicy):
    def has_permission(self, request, view):
        return super().has_permission(request, view)



"""___________________Admin Related Info__________________"""
class AdminContactInfoViewPolicy(BaseAdminOnlyPermissionPolicy):
    def has_permission(self, request, view):
        return super().has_permission(request, view)
