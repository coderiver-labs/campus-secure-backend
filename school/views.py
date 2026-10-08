from django.shortcuts import render
from django.db import transaction
from django.db.models import Model

# DRF
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny


# import base views 
from school.base_views import BaseSubjectViewSet, BaseClassLevelViewSet, BaseSectionViewSet
from school.base_views import BaseAboutViewSet

# models
from school.models import About


# import serializer
from rest_framework.serializers import Serializer
from school.serializers import AboutPublicSerializer

# import permission
from school.permissions.policy import SchoolManageViewPolicy
from school.permissions.policy import AboutViewPolicy

# import AuditLog
from audit.services import AuditService

# docs
from drf_spectacular.utils import extend_schema, extend_schema_view









# Create your views here.


# Subject ViewSet

@extend_schema_view(
    list=extend_schema(
        tags=["Subjects"],
        summary="List Subjects",
        description="Retrieve a list of school subjects with filtering, searching, and ordering support.",
    ),
    create=extend_schema(
        tags=["Subjects"],
        summary="Create Subject",
        description="Create a new school subject.",
    ),
    retrieve=extend_schema(
        tags=["Subjects"],
        summary="Retrieve Subject",
        description="Retrieve details of a specific school subject.",
    ),
    update=extend_schema(
        tags=["Subjects"],
        summary="Update Subject",
        description="Update an existing school subject.",
    ),
    partial_update=extend_schema(
        tags=["Subjects"],
        summary="Partially Update Subject",
        description="Partially update an existing school subject.",
    ),
)
class SubjectViewSet(BaseSubjectViewSet):
    permission_classes = [
        SchoolManageViewPolicy
        
    ]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        policy_class = self.permission_classes[0]
        return policy_class.scope_queryset(request=self.request, qs=queryset)
    
    def perform_create(self, serializer: Serializer):
        with transaction.atomic():
            instance = serializer.save()
            AuditService.create_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="Subject Created"
            )
            
    
    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()
            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Subject Updated"
            )
            serializer.save()
    




# ClassLevel ViewSet

@extend_schema_view(
    list=extend_schema(
        tags=["Class Levels"],
        summary="List Class Levels",
        description="Retrieve a list of class levels with filtering, searching, and ordering support.",
    ),
    create=extend_schema(
        tags=["Class Levels"],
        summary="Create Class Level",
        description="Create a new class level with its monthly fee and associated subjects.",
    ),
    retrieve=extend_schema(
        tags=["Class Levels"],
        summary="Retrieve Class Level",
        description="Retrieve details of a specific class level.",
    ),
    update=extend_schema(
        tags=["Class Levels"],
        summary="Update Class Level",
        description="Update an existing class level.",
    ),
    partial_update=extend_schema(
        tags=["Class Levels"],
        summary="Partially Update Class Level",
        description="Partially update an existing class level.",
    ),
)
class ClassLevelViewSet(BaseClassLevelViewSet):
    permission_classes = [
        SchoolManageViewPolicy
    ]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        policy_class = self.permission_classes[0]
        return policy_class.scope_queryset(request=self.request, qs=queryset)
    
    def perform_create(self, serializer: Serializer):
        with transaction.atomic():
            instance = serializer.save()
            AuditService.create_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="Class Level Created"
            )
            
    
    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()
            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Class Level Updated"
            )
            serializer.save()





from school.base_views import BaseSectionViewSet
@extend_schema_view(
    list=extend_schema(
        tags=["Sections"],
        summary="List Sections",
        description="Retrieve a list of school sections.",
    ),
    create=extend_schema(
        tags=["Sections"],
        summary="Create Section",
        description="Create a new school section.",
    ),
    retrieve=extend_schema(
        tags=["Sections"],
        summary="Retrieve Section",
        description="Retrieve details of a specific school section.",
    ),
    update=extend_schema(
        tags=["Sections"],
        summary="Update Section",
        description="Update an existing school section.",
    ),
    partial_update=extend_schema(
        tags=["Sections"],
        summary="Partially Update Section",
        description="Partially update an existing school section.",
    ),
)
class SectionViewSet(BaseSectionViewSet):
    permission_classes = [
        SchoolManageViewPolicy
    ]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        policy_class = self.permission_classes[0]
        return policy_class.scope_queryset(request=self.request, qs=queryset)
    
    def perform_create(self, serializer: Serializer):
        with transaction.atomic():
            instance = serializer.save()
            AuditService.create_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="Section Created"
            )
            
    
    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()
            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Section Updated"
            )
            serializer.save()

            

from school.base_views import BaseStudentClassViewSet
@extend_schema_view(
    list=extend_schema(
        tags=["Student Classes"],
        summary="List Student Classes",
        description="Retrieve a list of student classes.",
    ),
    create=extend_schema(
        tags=["Student Classes"],
        summary="Create Student Class",
        description="Create a new student class.",
    ),
    retrieve=extend_schema(
        tags=["Student Classes"],
        summary="Retrieve Student Class",
        description="Retrieve details of a specific student class.",
    ),
    update=extend_schema(
        tags=["Student Classes"],
        summary="Update Student Class",
        description="Update an existing student class.",
    ),
    partial_update=extend_schema(
        tags=["Student Classes"],
        summary="Partially Update Student Class",
        description="Partially update an existing student class.",
    ),
)
class StudentClassViewSet(BaseStudentClassViewSet):
    permission_classes = [
        SchoolManageViewPolicy
    ]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        policy_class = self.permission_classes[0]
        return policy_class.scope_queryset(request=self.request, qs=queryset)
    
    def perform_create(self, serializer: Serializer):
        with transaction.atomic():
            instance = serializer.save()
            AuditService.create_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="Student-Class Created"
            )
            
    
    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()
            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Student-Class Updated"
            )
            serializer.save()
    


# Admin Views
@extend_schema_view(
    list=extend_schema(
        tags=["About"],
        summary="List About Information",
        description="Retrieve the school about information.",
    ),
    retrieve=extend_schema(
        tags=["About"],
        summary="Retrieve About Information",
        description="Retrieve details of the school about information.",
    ),
    update=extend_schema(
        tags=["About"],
        summary="Update About Information",
        description="Update the school about information.",
    ),
    partial_update=extend_schema(
        tags=["About"],
        summary="Partially Update About Information",
        description="Partially update the school about information.",
    ),
)
class AboutViewSet(BaseAboutViewSet):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AboutViewPolicy]
    def get_queryset(self):
        queryset = super().get_queryset()
        policy_class = self.permission_classes[0]
        return policy_class.scope_queryset(request=self.request, qs=queryset)



# Public About Views
@extend_schema_view(
    list=extend_schema(
        tags=["About"],
        summary="List Public About Information",
        description="Retrieve publicly available school about information.",
    ),
    retrieve=extend_schema(
        tags=["About"],
        summary="Retrieve Public About Information",
        description="Retrieve publicly available details of the school.",
    ),
)
class PublicAboutViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = AboutPublicSerializer
    lookup_field = "uuid"
    queryset = About.objects.all()





