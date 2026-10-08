from django.shortcuts import render
from django.db import transaction
from django.db.models import Model

# import base_views
from students.base_views import BaseStudentProfileViewSet

# import serializer
from rest_framework.serializers import Serializer



# import AuditLog
from audit.services import AuditService

# docs
from drf_spectacular.utils import extend_schema, extend_schema_view


# Create your views here.

from students.permissions.policy import StudentProfileViewPolicy
@extend_schema_view(
    list=extend_schema(
        tags=["Student Profile & Academic"],
        summary="List Student Profiles",
        description=(
            "Retrieve a list of student profiles with support for "
            "filtering, searching, and ordering."
        ),
    ),
    retrieve=extend_schema(
        tags=["Student Profile & Academic"],
        summary="Retrieve Student Profile",
        description="Retrieve details of a specific student profile.",
    ),
    update=extend_schema(
        tags=["Student Profile & Academic"],
        summary="Update Student Profile",
        description="Update an existing student profile.",
    ),
    partial_update=extend_schema(
        tags=["Student Profile & Academic"],
        summary="Partially Update Student Profile",
        description="Partially update an existing student profile.",
    ),
)
class StudentProfileViewSet(BaseStudentProfileViewSet):
    permission_classes = [StudentProfileViewPolicy]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        policy_class = self.permission_classes[0]
        return policy_class.scope_queryset(request=self.request, qs=queryset)
    

    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()
            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Student Profile Updated"
            )
            serializer.save()


