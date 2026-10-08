from utils.base_view import BaseModelViewSet
from django.db.models import QuerySet

# DRF
from rest_framework.viewsets import ModelViewSet

from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import ValidationError

# import serializer
from exams.serializers import ExamSerializer

# import models
from exams.models import Exam, ExamClass, ExamSubject, StudentMark
from accounts.models import TeacherAssignment, StudentAcademicInfo



# create your base views hare


class BaseExamViewSet(BaseModelViewSet):
    
    
    filterset_fields = {
            "year": ["exact"],
            "status": ["iexact"],
            "is_active": ["exact"],
            "start_date": ["exact", "gte", "lte"],
            "end_date": ["exact", "gte", "lte"],
            "created_at": ["date", "gte", "lte"],
        }

    # '^' starts-with, '@'  full-text search
    search_fields = ["name", "description"]

    ordering_fields = ["year", "start_date", "end_date", "created_at"]
    # Default ordering    
    ordering = ["-created_at"]
    
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()





from exams.serializers import ExamClassWriteSerializer, ExamClassReadSerializer
class BaseExamClassesViewSet(BaseModelViewSet):

    # ২. filter (ForeignKey field ar upre vitti kore)
    filterset_fields = {
        # exam uuid diye filter kora jabe : ?exam=uuid_here
        "exam__uuid": ["exact"],
        "exam__year": ["exact"],
        "exam__is_active": ["exact"],

        # student class ar uuid diye shob exam dekhte parbe sei class ar kono exam ase naki: ?student_class=uuid_here
        "student_class__uuid": ["exact"],
        
        # exam ar status diyow check korte parbe : ?exam__status=ongoing
        "exam__status": ["iexact"],
    }

    search_fields = [
        "exam__name", 
        "student_class__student_class__name", # ClassLevel name diyew serch korte parbe jemon ?search=six 
        "student_class__section__section"    # Section diyew search korte parbe jemon ?search=A
    ]

    # ordering
    ordering_fields = ["created_at", "exam__year"]
    ordering = ["-created_at"]
    
    
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ExamClassWriteSerializer
        return ExamClassReadSerializer


    queryset = ExamClass.objects.all()
    lookup_field = "uuid"




from exams.serializers import ExamSubjectReadSerializer, ExamSubjectWriteSerializer
from exams.filtering import ExamSubjectFilter, StudentMarkFilter
class BaseExamSubjectViewSet(BaseModelViewSet):

    filterset_class = ExamSubjectFilter
    
    search_fields = ["exam_class__exam__name", "subject__name", "full_mark", "pass_mark"]
    ordering_fields = ["created_at", "updated_at", "full_mark", "-full_mark", "pass_mark", "-pass_mark"]
    ordering = ["-created_at"]

    
    
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ExamSubjectWriteSerializer
        return ExamSubjectReadSerializer
    
    queryset = ExamSubject.objects.all()





from exams.serializers import StudentMarkSerializer, StudentMarkReadSerializer
class BaseStudentMarkViewSet(BaseModelViewSet):
    filterset_class = StudentMarkFilter
        
    # Search Fields: text to search
    search_fields = [
        "student__user__first_name", 
        "student__user__last_name", 
        "student__roll_number",
        "exam_subject__subject__name",
        "exam_subject__exam_class__exam__name"
    ]
    
    # Ordering Fields
    ordering_fields = [
        "marks_obtained", 
        "created_at", 
        "updated_at",
        "student__roll_number"
    ]
    
    # Default Ordering
    ordering = ["-created_at"]


    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return StudentMarkSerializer
        return StudentMarkReadSerializer
        
    queryset = StudentMark.objects.all()

    def get_queryset(self):
        queryset: QuerySet = super().get_queryset().select_related(
            "student__user",
            "student__academic_info__student_class__student_class_level",
            "exam_subject__subject", # serializer ar moddhe exam_subject ar name show korar jonno 
        )
        
        policy_class = self.permission_classes[0]
        qs = policy_class.scope_queryset(request=self.request, qs=queryset)
        return qs





from exams.serializers import ExamCandidateSerializer
from exams.helpers import get_exam_subject
class BaseExamCandidateAPIView(GenericAPIView):
    serializer_class = ExamCandidateSerializer

    def get_queryset(self):
        exam_subject_uuid = self.request.query_params.get("exam_subject") 
        if not exam_subject_uuid:
            raise ValidationError({"exam_subject": "This query parameter is required."})


        status = self.request.query_params.get("status", "remaining")
        exam_subject = get_exam_subject(pk=exam_subject_uuid)

        user = self.request.user
        # akhne onek kajj korte hobe , filtering optimize r "superuser, admin" ar jonno query. aro onek kisu
        # akhon time nei tai teacher ar jonno iktu kahni kore rakhlam. r akhne ekoi jini s onek ase , abar response a onek kisu add korte hobe jemon kono jon "mark peyese, kotojon paini" tar akta shonkha
        if user.is_superuser or user.role == "admin":
            student = StudentMark.objects.filter(exam_subject=exam_subject).values_list("student", flat=True)
            return StudentAcademicInfo.objects.filter(student__in=student)
        

         


        # jodi teacher kono vabe onno exam_subject ar uuid diye try kore aijonno teacher ar policy check
        assignments = TeacherAssignment.objects.filter(teacher=user.teacher_profile)
        # if assignments.filter(subject_id__in=exam_subject.subject.uuid).exist():
        if assignments.filter(
            subject_id=exam_subject.subject_id,
            student_class_id=exam_subject.exam_class.student_class_id,
        ).exists():
            
            student_info = StudentAcademicInfo.objects.filter(
                student_class=exam_subject.exam_class.student_class
            ).select_related("student", "student__user") # exam subject ar student gular list
            
            student_mark = StudentMark.objects.filter(exam_subject__exam_class__exam__is_active=True)
            assign_mark_students = student_mark.filter(exam_subject=exam_subject).values_list("student", flat=True)
            # assign_mark_students = StudentMark.objects.filter(exam_subject=exam_subject).values_list("student", flat=True)
            if status == "remaining":
                remaining_student = student_info.exclude(student_id__in=assign_mark_students)
                return remaining_student

            if status == "completed":
                return student_info.filter(student_id__in=assign_mark_students)
            if status == "all":
                return student_info # student profile ke return korsi 

            



