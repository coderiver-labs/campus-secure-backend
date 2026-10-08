# import base views
from utils.base_view import BaseSchoolViewSet

# DRF
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

# import models
from school.models import Subject, ClassLevel, Sections, StudentClass, About

# import serializers
from school.serializers import SubjectSerializer, ClassLevelSerializer, SectionSerializer, AboutAdminSerializer


# create your base view



class BaseSubjectViewSet(BaseSchoolViewSet):
    filterset_fields = {
        "name": ["iexact"],
        "code": ["exact"],
        "is_active": ["exact"]
    }
    search_fields = ["name", "description"]
    ordering_fields = ["is_active", "created_at", "updated_at"]
    ordering = ["-created_at"]
    
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


# ClassLevel ViewSet
class BaseClassLevelViewSet(BaseSchoolViewSet):
    
    filterset_fields = {
        "name": ["exact"],
        "monthly_fee": ["exact", "icontains"],
        "subjects": ["exact"],
        "subjects__name": ["iexact", "icontains"],

    }
    
    search_fields = ["name", "monthly_fee"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    serializer_class = ClassLevelSerializer
    queryset = ClassLevel.objects.prefetch_related("subjects")



class BaseSectionViewSet(BaseSchoolViewSet):
    
    serializer_class = SectionSerializer
    queryset = Sections.objects.all()
    
    

from school.serializers import StudentClassSerializer, StudentClassListSerializer

class BaseStudentClassViewSet(BaseSchoolViewSet):

    def get_serializer_class(self):
        match self.request.method:
            case "POST" | "PUT" | "PATCH":
                return StudentClassSerializer
            case _:
                return StudentClassListSerializer
            
    queryset = StudentClass.objects.all()




class BaseAboutViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = AboutAdminSerializer
    lookup_field = "uuid"
    queryset = About.objects.all()



