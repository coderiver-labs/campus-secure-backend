from django.db.models.query import QuerySet

# DRF
from rest_framework.request import Request

# import packages
from rest_access_policy.access_policy import AccessPolicy


# import models 
from accounts.models import CustomUser

# import utils
from utils.decorator.permissions import default_allow_admin_and_superuser
from utils.permissions.services import check_staff_permission

# create access policy hare



class StudentProfileViewPolicy(AccessPolicy):

    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": ["authenticated",],
            "effect": "allow",
            "condition": ["can_list_retrieve_student_profile"]
        },
        {
            "action": ["update", "partial_update"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["can_update_partial_update"]
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
            
        return qs.none()

    @default_allow_admin_and_superuser
    def can_list_retrieve_student_profile(self, request: Request, view, action):
        user: CustomUser = request.user

        staff_position = ["manager", "principal"]
        if user.role == "staff":
            return check_staff_permission(user=user, positions=staff_position)
        return False
    


    @default_allow_admin_and_superuser
    def can_update_partial_update(self, request: Request, view, action):
        return False