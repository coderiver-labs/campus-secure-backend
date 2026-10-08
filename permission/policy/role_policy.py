from django.core.exceptions import ImproperlyConfigured
from permission.core.policy_engine import PolicyEngine

# DRF
from rest_framework.viewsets import ViewSet
from rest_framework.request import HttpRequest

# import base permission
from permission.core.base import BasePermissionWithBypass

# import models
from accounts.models import CustomUser

# import utils
from utils.policy_loader import get_policy



# create Policy hare


class RolePolicyPermission(BasePermissionWithBypass):

    def check_permission(self, request: HttpRequest, view:ViewSet):
        user: CustomUser = request.user
        
        if user.is_anonymous:
            return False
        
        permission_key = getattr(view, "permission_key", None)
        action = getattr(view, "action", None)

        if not action:
            return False
            
        if not permission_key:
            raise ImproperlyConfigured(
                f"{view.__class__.__name__} missing permission_key"
            )
            

        engine = PolicyEngine(get_policy())

        return engine.evaluate(
            permission_key=permission_key,
            role=user.role,
            action=action,
            user=user
        )