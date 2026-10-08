from django.shortcuts import render
from rest_framework.generics import GenericAPIView

# import base view
from audit.base_views import BaseAuditView

# import serializer
from audit.serializers import AuditLogSerializer

# import models 
from audit.models import AuditLog

# import permission
from permission.policy.role_policy import RolePolicyPermission

# docs
from drf_spectacular.utils import extend_schema, extend_schema_view

# Create your views here.


@extend_schema_view(
    list=extend_schema(
        tags=["Audit Logs"],
        summary="List Audit Logs",
        description=(
            "Retrieve a list of audit logs with support for filtering, "
            "searching, and ordering."
        ),
    ),
    retrieve=extend_schema(
        tags=["Audit Logs"],
        summary="Retrieve Audit Log",
        description="Retrieve details of a specific audit log.",
    ),
)
class AuditView(BaseAuditView):
    
    permission_classes = [RolePolicyPermission]
    permission_key = "audit"
    lookup_field = "uuid"

    def get_queryset(self):
        return AuditLog.objects.all()
    
    