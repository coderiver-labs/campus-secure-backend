# DRF
from rest_framework.request import HttpRequest, Request

# DRF_Permission_policy
from rest_access_policy.access_policy import AccessPolicy

# import models
from accounts.models import CustomUser, TeacherAssignment
from exams.models import ExamClass, ExamSubject, StudentMark

# import view
from exams.base_views import BaseStudentMarkViewSet

# import utils
from utils.permissions.services import check_staff_permission


from utils.decorator.permissions import default_allow_admin_and_superuser, default_allow_superuser
from django.db.models.query import QuerySet
from typing import Any

# create your policy



from rest_access_policy.access_policy import AccessPolicy
class ExamAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["can_view_exams"]
        },
        {
            "action": ["create", "update", "partial_update", "destroy"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["can_manage_exams"]
        }
    ]

    @default_allow_admin_and_superuser
    def can_view_exams(self, request: Request, view, action):
        user: CustomUser = request.user

        staff_positions = ["manager", "principal"]
        if user.role == "staff":
            return check_staff_permission(user=request.user, positions=staff_positions)

        if user.role == "teacher": 
            return True
        return False

    @default_allow_admin_and_superuser
    def can_manage_exams(self, request: Request, view, action):
        return False


    @classmethod
    def scope_queryset(cls, request: Request, qs: QuerySet[Any]) -> QuerySet[Any]:
        user: CustomUser = request.user
        if user.is_superuser or user.role == "admin":
            return qs
        staff_positions = ["manager", "principal"]

        if user.role == "staff":
            check_staff_permission(user=user, positions=staff_positions)
            return qs.filter(is_active=True)
        
        if user.role == "teacher":
            return qs.filter(is_active=True)

        return qs.none()
            



class ExamClassesViewSetPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["can_view_exam_classes"]
        },
        {
            "action": ["create", "update", "partial_update", "destroy"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["can_manage_exam_classes"]
        }
    ]
    staff_positions = ["manager", "principal"]
    
    @classmethod
    def scope_queryset(cls, request: Request, qs: QuerySet[ExamClass]) -> QuerySet[ExamClass]:
        user: CustomUser = request.user
        if user.is_superuser or user.role == "admin":
            return qs
        
        if user.role == "staff":
            check_staff_permission(user=user, positions=cls.staff_positions)
            return qs.filter(exam__is_active=True)
        
        queryset = qs.filter(exam__is_active=True)
        if user.role == "teacher":
            student_class = TeacherAssignment.objects.filter(teacher=user.teacher_profile).values_list("student_class")
            return queryset.filter(student_class__in=student_class)
        
        if user.role == "student":
            return queryset.filter(student_class=user.student_profile.academic_info.student_class)
        return qs.none()


    @default_allow_admin_and_superuser
    def can_view_exam_classes(self, request: Request, view, action):
        user: CustomUser = request.user
        if user.role == "staff":
            return check_staff_permission(user=user, positions=self.staff_positions)
        if user.role == "teacher" or user.role == "student":
            return True
        return False
    
    @default_allow_admin_and_superuser
    def can_manage_exam_classes(self, request: Request, view, action):
        user: CustomUser = request.user
        if user.role == "staff":
            return check_staff_permission(user=user, positions=self.staff_positions)
        return False

    


class ExamSubjectAccessPolicy(AccessPolicy):

    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["can_view_exam_subject"]
        },
        {
            "action": ["create", "update", "partial_update", "destroy"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["can_manage_exam_subject"]
        }
    ]

    staff_positions = ["manager", "principal"]

    @default_allow_admin_and_superuser
    def can_view_exam_subject(self, request: Request, view, action):
        user: CustomUser = request.user

        staff_positions = ["manager", "principal"]
        if user.role == 'staff':
            return check_staff_permission(user=user, positions=staff_positions)
        
        if user.role == "teacher" or user.role == "student":
            return True

        
        return False
    
    @default_allow_admin_and_superuser
    def can_manage_exam_subject(self, request: Request, view, action):
        user: CustomUser = request.user

        if user.role == "staff":
            return check_staff_permission(user=user, positions=self.staff_positions)
        return False
    

    @classmethod
    def scope_queryset(cls, request: Request, qs: QuerySet[any])-> QuerySet[Any]:
        user: CustomUser = request.user 
        if user.is_superuser or user.role == "admin":
            return qs
        
        qs = qs.filter(exam_class__exam__status__in=["draft", "ongoing"], exam_class__exam__is_active=True)
        
        if user.role == "student":
            if hasattr(user, "student_profile") and user.student_profile.academic_info.student_class:
                student_current_class = user.student_profile.academic_info.student_class
                return qs.filter(exam_class__student_class=student_current_class)

        from accounts.models import TeacherAssignment
        if user.role == "teacher":
            assignments = TeacherAssignment.objects.filter(teacher=user.teacher_profile).values(
                "student_class_id",
                "subject_id"
            )
            if not assignments:
                return qs.none()

            from django.db.models import Q
            filters = Q()

            for assignment in assignments:
                filters |= Q(
                    exam_class__student_class_id=assignment["student_class_id"],
                    subject_id=assignment["subject_id"],
                )
            return qs.filter(filters)
        return qs.none()





class StudentMarkViewSetAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["can_view_exam_mark"],
        },
        {
            "action": ["create"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["can_create_exam_mark"],
        },
        {
            "action": ["update", "partial_update"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["can_update_exam_mark"],
        },
        {
            "action": ["destroy"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["can_delete_exam_mark"],
        },
    ]

    @classmethod
    def scope_queryset(cls, request: Request, qs: QuerySet):
        user: CustomUser = request.user

        if user == "superuser" or user.role == "admin":
            return qs

        staff_positions = ["principal", "vice_principal", "manager"]
        if user.role == 'staff':
            if check_staff_permission(user=user, positions=staff_positions):
                return qs

        qs = qs.filter(exam_subject__exam_class__exam__is_active=True)
        if user.role == "student":
            query = qs.filter(exam_subject__exam_class__exam__status="published")
            return query.filter(student__user=user)

        from django.db.models import Q
        from accounts.models import TeacherAssignment
        if user.role == "teacher":
            assignments = TeacherAssignment.objects.filter(
                teacher__user=user
            ).values(
                "student_class_id",
                "subject_id",
            )

            if not assignments:
                return qs.none()

            filters = Q()

            for assignment in assignments:
                filters |= Q(
                    exam_subject__exam_class__student_class_id=assignment["student_class_id"],
                    exam_subject__subject_id=assignment["subject_id"],
                )
            return qs.filter(filters)
        return qs.none()
    
    @default_allow_admin_and_superuser
    def can_view_exam_mark(self, request: Request, view, action):
        user: CustomUser = request.user

        if user.role == "staff":
            staff_positions = ["manager", "principal"]
            if check_staff_permission(user=user, positions=staff_positions):
                return True
        
        if user.role == "teacher":
            return True
        
        if user.role == "student":
            return True
        
        return False
    
    @default_allow_admin_and_superuser
    def can_create_exam_mark(self, request: Request, view, action):
        user: CustomUser = request.user

        if user.role == "teacher":
            return True
        return False
    
    @default_allow_admin_and_superuser
    def can_update_exam_mark(self, request: Request, view, action):
        user: CustomUser = request.user
        
        if user.role == "teacher":
            return True
        return False

    @default_allow_admin_and_superuser
    def can_delete_exam_mark(self, request: Request, view, action):
        return False
    


from rest_access_policy.access_policy import AccessPolicy
from rest_framework.permissions import BasePermission
class ExamCandidateAPIViewSetPolicy(BasePermission):
    def has_permission(self, request: Request, view):
        user: CustomUser = request.user
        if user.is_superuser or user.role == "admin":
            return True
        if user.role in ["teacher",]:
            return True
        return False
    
