from django.db import transaction

# import base view
from exams.base_views import (
    BaseExamViewSet, 
    BaseExamClassesViewSet, 
    BaseExamSubjectViewSet, 
    BaseStudentMarkViewSet
)

# import models
from exams.models import Exam, ExamClass

# import serializers
from rest_framework.serializers import Serializer

# import permission 
from .permission.policy import ExamAccessPolicy, ExamSubjectAccessPolicy


# Audit Log
from audit.services import AuditService

# docs
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes


# Create your views here.


        
# Exam ViewSet


@extend_schema_view(
    list=extend_schema(
        tags=["Exam Management"],
        summary="List Exams",
        description="Retrieve a list of exams with filtering, searching, and ordering support.",
    ),
    create=extend_schema(
        tags=["Exam Management"],
        summary="Create Exam",
        description="Create a new exam.",
    ),
    retrieve=extend_schema(
        tags=["Exam Management"],
        summary="Retrieve Exam",
        description="Retrieve details of a specific exam.",
    ),
    update=extend_schema(
        tags=["Exam Management"],
        summary="Update Exam",
        description="Update an existing exam.",
    ),
    partial_update=extend_schema(
        tags=["Exam Management"],
        summary="Partially Update Exam",
        description="Partially update an existing exam.",
    ),
    destroy=extend_schema(
        tags=["Exam Management"],
        summary="Delete Exam",
        description="Delete an existing exam.",
    ),
)
class ExamViewSet(BaseExamViewSet):
    permission_classes = [ExamAccessPolicy,]

    def get_queryset(self):
        policy_class = self.permission_classes[0]
        return policy_class.scope_queryset(self.request, super().get_queryset())

    def perform_create(self, serializer: Serializer):
        with transaction.atomic():
                
            instance = serializer.save()
            AuditService.create_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="Exam Created"
            )
            
    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()            

            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Exam Updated"
            )
            serializer.save()
            
    def perform_destroy(self, instance: Exam):
        with transaction.atomic():
            
            AuditService.delete_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="Exam Deleted"
            )
            instance.delete()
            
            

from exams.permission.policy import ExamClassesViewSetPolicy
# Exam-Class ViewSet

@extend_schema_view(
    list=extend_schema(
        tags=["Exam Classes"],
        summary="List Exam Classes",
        description="Retrieve a list of exam classes with filtering, searching, and ordering support.",
    ),
    create=extend_schema(
        tags=["Exam Classes"],
        summary="Create Exam Class",
        description="Create a new exam class.",
    ),
    retrieve=extend_schema(
        tags=["Exam Classes"],
        summary="Retrieve Exam Class",
        description="Retrieve details of a specific exam class.",
    ),
    update=extend_schema(
        tags=["Exam Classes"],
        summary="Update Exam Class",
        description="Update an existing exam class.",
    ),
    partial_update=extend_schema(
        tags=["Exam Classes"],
        summary="Partially Update Exam Class",
        description="Partially update an existing exam class.",
    ),
    destroy=extend_schema(
        tags=["Exam Classes"],
        summary="Delete Exam Class",
        description="Delete an existing exam class.",
    ),
)
class ExamClassesViewSet(BaseExamClassesViewSet):
    permission_classes = [ExamClassesViewSetPolicy]

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
                description="Exam Class Created"
            )
            
    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()            

            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Exam Class Updated"
            )
            serializer.save()
            
    def perform_destroy(self, instance: ExamClass):
        with transaction.atomic():
            
            AuditService.delete_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="Exam Class Deleted"
            )
            instance.delete()






# Exam SubjectViewSet
@extend_schema_view(
    list=extend_schema(
        tags=["Exam Subjects"],
        summary="List Exam Subjects",
        description="Retrieve a list of exam subjects with filtering, searching, and ordering support.",
    ),
    create=extend_schema(
        tags=["Exam Subjects"],
        summary="Create Exam Subject",
        description="Create a new exam subject.",
    ),
    retrieve=extend_schema(
        tags=["Exam Subjects"],
        summary="Retrieve Exam Subject",
        description="Retrieve details of a specific exam subject.",
    ),
    update=extend_schema(
        tags=["Exam Subjects"],
        summary="Update Exam Subject",
        description="Update an existing exam subject.",
    ),
    partial_update=extend_schema(
        tags=["Exam Subjects"],
        summary="Partially Update Exam Subject",
        description="Partially update an existing exam subject.",
    ),
    destroy=extend_schema(
        tags=["Exam Subjects"],
        summary="Delete Exam Subject",
        description="Delete an existing exam subject.",
    ),
)
class ExamSubjectViewSet(BaseExamSubjectViewSet):
    permission_classes = [ExamSubjectAccessPolicy,]
    
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
                description="Exam Subject Created"
            )
            
    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()            

            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Exam Subject Updated"
            )
            serializer.save()
            
    def perform_destroy(self, instance: ExamClass):
        with transaction.atomic():
            
            AuditService.delete_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="Exam Subject Deleted"
            )
            instance.delete()



from rest_framework import status
from exams.base_views import BaseStudentMarkViewSet
from exams.permission.policy import StudentMarkViewSetAccessPolicy
from exams.permission.authorizers import StudentMarkAuthorizer
from exams.serializers import StudentMarkSerializer, StudentMarkReadSerializer

@extend_schema_view(
    list=extend_schema(
        tags=["Exam Candidates & Marks"],
        summary="List student marks",
        description="Retrieve a list of student marks.",
        responses={status.HTTP_200_OK: StudentMarkReadSerializer(many=True)}
    ),
    retrieve=extend_schema(
        tags=["Exam Candidates & Marks"],
        summary="Retrieve a student mark",
        description="Retrieve detailed information about a specific student mark.",
        responses={status.HTTP_200_OK: StudentMarkReadSerializer}
    ),
    create=extend_schema(
        tags=["Exam Candidates & Marks"],
        summary="Create a student mark",
        description="Create a new mark record for a student.",
        responses={status.HTTP_201_CREATED: StudentMarkSerializer}
    ),
    update=extend_schema(
        tags=["Exam Candidates & Marks"],
        summary="Update a student mark",
        description="Update an existing student mark.",
        responses={status.HTTP_200_OK: StudentMarkSerializer}
    ),
    partial_update=extend_schema(
        tags=["Exam Candidates & Marks"],
        summary="Partially update a student mark",
        description="Partially update an existing student mark.",
        responses={status.HTTP_200_OK: StudentMarkSerializer}
    ),
    destroy=extend_schema(
        tags=["Exam Candidates & Marks"],
        summary="Delete a student mark",
        description="Delete an existing student mark.",
        responses={status.HTTP_204_NO_CONTENT: None},
    )

)
class StudentMarkViewSet(BaseStudentMarkViewSet):
    permission_classes = [StudentMarkViewSetAccessPolicy,]

    def perform_create(self, serializer: Serializer):
        exam_subject = serializer.validated_data["exam_subject"]
        StudentMarkAuthorizer.authorize_create(user=self.request.user, exam_subject=exam_subject)

        with transaction.atomic():
            instance = serializer.save()
            AuditService.create_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="Student Mark Created"
            )
            
    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()            
            StudentMarkAuthorizer.authorize_update(user=self.request.user, instance=instance)
            
            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="Student Mark Updated"
            )
            serializer.save()
            
    def perform_destroy(self, instance: ExamClass):
        with transaction.atomic():
            
            AuditService.delete_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="Student Mark Deleted"
            )
            instance.delete()





from exams.permission.policy import ExamCandidateAPIViewSetPolicy
from exams.base_views import BaseExamCandidateAPIView

@extend_schema(
    tags=["Exam Candidates & Marks"],
    summary="List Exam Candidates",
    description=(
        "Retrieve students associated with an exam subject. "
        "Candidates can be filtered by their mark completion status."
    ),
    parameters=[
        OpenApiParameter(
            name="exam_subject",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            required=True,
            description="UUID of the exam subject.",
        ),
        OpenApiParameter(
            name="status",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            enum=["remaining", "completed", "all"],
            default="remaining",
            description="Filter candidates by mark completion status.",
        ),
    ],
)
class ExamCandidateAPIViewSet(BaseExamCandidateAPIView):
    
    permission_classes = [
        ExamCandidateAPIViewSetPolicy
    ]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(queryset=serializer.data)
        return self.get_paginated_response(data=page)
    