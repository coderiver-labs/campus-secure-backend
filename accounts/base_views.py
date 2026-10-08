from django.db.models import Q
from django.db.models import QuerySet

# DRF
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.throttling import ScopedRateThrottle

# import models 
from accounts.models import CustomUser
from accounts.models import AdminProfile
from accounts.models import StaffProfile
from accounts.models import TeacherAssignment, TeacherProfile, TeacherContactInfo, TeacherProfessionalInfo
from accounts.models import (
    StudentProfile,
    StudentAcademicInfo,
    StudentContactInfo,
    StudentParentsInfo,
    StudentHealthInfo,
)



# import serializer
from accounts.serializers import (
    CustomUserCreateSerializer,
    CustomUserUpdateSerializer,
)
from accounts.serializers import (
    # GET
    CustomUserForTeacherViewSerializer, 
    CustomUserForStaffViewSerializer, 
    CustomUserForStudentViewSerializer, 
    CustomUserForSuperUserAndAdminViewSerializer
)
# import base views 
from utils.base_view import BaseModelViewSet, BasePublicModelViewSet, BaseUserRelatedInfoView 

# python and hint
from typing import cast



# create accounts base views hare




class BaseUserManagementView(BaseModelViewSet):
    
    filterset_fields = {
        "first_name": ["iexact", "istartswith", "icontains"],
        "last_name": ["iexact", "istartswith", "icontains"],
        "email": ["exact", "iexact", "istartswith", "icontains"],
        "role": ["iexact"],
        "is_active": ["exact"],
        "created_at": ["date", "gte", "lte"],
    }
    
    search_fields = [
        "^first_name",
        "^last_name",
        "^email",
    ]

    ordering_fields = [
        "created_at",
        "first_name",
        "last_name",
        "email",
    ]
    
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            user: CustomUser = self.request.user

            if user.role == "student":
                return CustomUserForStudentViewSerializer

            if user.role == "teacher":
                return CustomUserForTeacherViewSerializer

            if user.role == "staff":
                return CustomUserForStaffViewSerializer

            if user.role == "admin" or user.is_superuser:
                return CustomUserForSuperUserAndAdminViewSerializer

        if self.action == "create":
            return CustomUserCreateSerializer

        if self.action in ["update", "partial_update"]:
            return CustomUserUpdateSerializer


    
    def get_queryset(self) -> QuerySet[CustomUser]:
        user: CustomUser = self.request.user
        
        qs = cast(QuerySet, super().get_queryset()).select_related(
            "student_profile",
            "teacher_profile", 
            # "teacher_profile__subject",  
            "staff_profile",
            "staff_profile__position",  
            "admin_profile"
        )

        if user.is_superuser:
            return qs

        if user.role == "admin":
            return qs.filter(
                Q(role__in=["staff", "teacher", "student"]) | Q(uuid=user.uuid)
            )

        if user.role == "staff":
            return qs.filter(
                Q(role__in=["teacher", "student"]) | Q(uuid=user.uuid)
            )

        if user.role == "teacher":
            teacher_profile = getattr(user, "teacher_profile", None)
            if not teacher_profile:
                return qs.none()

            from accounts.models import TeacherAssignment
            teacher_classes = TeacherAssignment.objects.filter(teacher=teacher_profile).values_list("student_class", flat=True)
            return qs.filter(
                student_profile__academic_info__student_class__in=teacher_classes
            )

        if user.role == "student":
            return qs.filter(uuid=user.uuid)

        return qs.none()



from accounts.serializers import TeacherAssignmentListRetrieveSerializer, TeacherAssignmentCreateUpdateSerializer
class BaseTeacherAssignmentViewSet(BaseModelViewSet):

    queryset = TeacherAssignment.objects.select_related(
        "teacher__user",
        "student_class__student_class_level",
        "student_class__section",
        "subject"
    )

    filterset_fields = {
        "teacher__user__first_name": ["iexact"],
        "teacher__user__last_name": ["iexact"],
        "student_class__student_class_level__name": ["exact"],
        "subject__name": ["iexact"],
        "subject__code": ["exact"]
    }

    search_fields = [
        "teacher__user__first_name",
        "teacher__user__last_name",
        "teacher__user__email",
        "student_class__student_class_level__name",
        "subject__name",
        "subject__code",
    ]

    ordering_fields = [
        "created_at",
        "teacher__user__first_name",
        "student_class__student_class_level__name",
        "subject__name",
    ]
    ordering = ["-created_at"]  # Default ordering

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TeacherAssignmentCreateUpdateSerializer
        return TeacherAssignmentListRetrieveSerializer


from accounts.serializers import (StudentProfileSerializer,  TeacherProfileSerializer, StaffProfileSerializer, AdminProfileSerializer)
from utils.serializers import DummySerializer
from django.db.models import Prefetch
class BaseProfileAPIView(RetrieveModelMixin, GenericAPIView):

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "api"

    def get_serializer_class(self):
        user: CustomUser = self.request.user
        if user.is_superuser:
            return DummySerializer
        
        match user.role:
            case "student":
                return StudentProfileSerializer
            case "teacher":
                return TeacherProfileSerializer
            case "staff":
                return StaffProfileSerializer
            case "admin":
                return AdminProfileSerializer

    def get_object(self):
        user: CustomUser = self.request.user
        if user.is_superuser:
            return None

        
        match user.role:
            case "student":
                return StudentProfile.objects.select_related(
                    "user",
                    "academic_info",
                    "parents_info",
                    "contact_info",
                    "health_info"
                ).get(user=user)

            case "teacher":
                return TeacherProfile.objects.select_related(
                    "user",
                    "professional_info",
                    "contact_info",
                ).prefetch_related(Prefetch(
                    "assignments",
                    queryset=TeacherAssignment.objects.select_related(
                        "student_class__student_class_level",
                        "subject"
                    )
                )).get(user=user)
            case "staff":
                return StaffProfile.objects.select_related(
                    "user",
                    "contact_info"
                ).prefetch_related("position",).get(user=user)
            

            case "admin":
                return AdminProfile.objects.select_related("user", "contact_info").get(user=user)

            case _:
                return None



"""________________Student Related Info__________________"""



from accounts.serializers import StudentAcademicInfoUpdateSerializer, StudentAcademicInfoGETSerializer
from accounts.filtering import StudentAcademicInfoFilter
class BaseStudentAcademicInfoView(BaseUserRelatedInfoView):
    filterset_class = StudentAcademicInfoFilter

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return StudentAcademicInfoUpdateSerializer
        return StudentAcademicInfoGETSerializer
    
    search_fields = [
        "student__user__first_name",
        "student__user__last_name",
        "student_class__student_class_level__name",
    ]
    ordering_fields = [
        "created_at",
        "updated_at",
        "start_year",
        "end_year",
    ]   
    ordering = ["-created_at"]

    def get_queryset(self):
        return StudentAcademicInfo.objects.select_related(
            "student",
            "student__user",
            "student_class",
            "student_class__student_class_level"
        )


from accounts.serializers import StudentParentsInfoGetSerializer, StudentParentsInfoUpdateSerializer
from accounts.filtering import StudentParentsInfoViewFilter
class BaseStudentParentsInfoView(BaseUserRelatedInfoView):

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return StudentParentsInfoGetSerializer
        return StudentParentsInfoUpdateSerializer
    
    def get_queryset(self):
        return StudentParentsInfo.objects.select_related("student", "student__user")
    
    filterset_class = StudentParentsInfoViewFilter
    search_fields = [
        "father_name",
        "mother_name",
        "father_phone",
        "mother_phone",
    ]
    ordering = ["-created_at"]



from accounts.serializers import  StudentContactInfoGetSerializer, StudentContactInfoUpdateSerializer
class BaseStudentContactInfoView(BaseUserRelatedInfoView):
    
    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return StudentContactInfoUpdateSerializer
        return StudentContactInfoGetSerializer
    
    def get_queryset(self):
        return StudentContactInfo.objects.select_related("student", "student__user")
    
    filterset_fields = {"phone": ["exact"], "address": ["iexact", "icontains"]}
    search_fields = ["phone", "address",]
    ordering = ["-created_at"]



from accounts.serializers import StudentHealthInfoGetSerializer, StudentHealthInfoUpdateSerializer
class BaseStudentHealthInfoView(BaseUserRelatedInfoView):

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return StudentHealthInfoUpdateSerializer
        return StudentHealthInfoGetSerializer
    
    def get_queryset(self):
        return StudentHealthInfo.objects.select_related("student", "student__user")
    
    
    filterset = {
        "blood_group": ["exact"],
        "height_cm": ["exact"],
        "weight_kg": ["exact"],
        "allergies": ["exact"],
        "medical_condition": ["exact"],

    }
    search_fields = [
        "student__user",
        "student__user__email",
        "student__user__first_name",
        "student__user__last_name",

    ]

    ordering = ["-created_at"]




"""___________________Teacher Related Info___________________"""

from accounts.serializers import TeacherContactInfoGetSerializer, TeacherContactInfoUpdateSerializer
class BaseTeacherContactInfoView(BaseUserRelatedInfoView):
    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return TeacherContactInfoUpdateSerializer
        return TeacherContactInfoGetSerializer

    def get_queryset(self):
        return TeacherContactInfo.objects.select_related("teacher", "teacher__user")
    
    filterset_fields = {"phone": ["exact"], "address": ["iexact", "icontains"]}
    search_fields = ["phone", "address",]
    ordering = "-created_at"


from accounts.serializers import TeacherProfessionalInfoGetSerializer, TeacherProfessionalInfoUpdateSerializer
class BaseTeacherProfessionalInfoView(BaseUserRelatedInfoView):
    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return TeacherProfessionalInfoUpdateSerializer
        return TeacherProfessionalInfoGetSerializer
    
    def get_queryset(self):
        return TeacherProfessionalInfo.objects.select_related("teacher", "teacher__user")
    
    filterset_fields = {
        "qualification": ["iexact"],
        "years_of_experience": ["iexact"],
        "subjects_specialization": ["iexact"],
        "education_qualification": ["iexact"],
    }

    search_fields = [
        "qualification",
        "years_of_experience",
        "subjects_specialization",
        "education_qualification",
    ]
    ordering = ["-created_at"]



"""__________________Staff Related Info_________________"""

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from accounts.models import StaffPosition
from accounts.serializers import StaffPositionSerializer

class BaseStaffPositionView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    def get_serializer_class(self):
        return StaffPositionSerializer

    def get_queryset(self):
        return StaffPosition.objects.all()
    
    lookup_field = "uuid"

    ordering = ["-name"]



from accounts.models import StaffContactInfo
from accounts.serializers import StaffContactInfoGetSerializer, StaffContactInfoUpdateSerializer
class BaseStaffContactInfoView(BaseUserRelatedInfoView):
    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return StaffContactInfoUpdateSerializer
        return StaffContactInfoGetSerializer
        
    def get_queryset(self):
        return StaffContactInfo.objects.select_related("staff", "staff__user")

    filterset_fields = {"phone": ["exact"], "address": ["iexact", "icontains"]}
    search_fields = ["phone", "address",]
    ordering = "-created_at"





"""_________________Admin Related Info_________________"""
from accounts.models import AdminContactInfo
from accounts.serializers import AdminContactInfoGetSerializer, AdminContactInfoUpdateSerializer
class BaseAdminContactView(BaseUserRelatedInfoView):
    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return AdminContactInfoUpdateSerializer
        return AdminContactInfoGetSerializer
        
    def get_queryset(self):
        return AdminContactInfo.objects.select_related("admin", "admin__user")

    filterset_fields = {"phone": ["exact"], "address": ["iexact", "icontains"]}
    search_fields = ["phone", "address",]
    ordering = "-created_at"
