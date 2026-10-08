from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request

# import models
from exams.models import ExamSubject
from accounts.models import TeacherProfile, TeacherAssignment
from exams.models import StudentMark



# class StudentMarkAuthorizer:

#     @classmethod
#     def authorize_create(cls, *, user, exam_subject):
#         """
#         Raise PermissionDenied if user cannot create
#         marks for the given ExamSubject.
#         """

#         if user.is_superuser or user.role == "admin":
#             return

#         if user.role != "teacher":
#             raise PermissionDenied(
#                 "You do not have permission to create marks."
#             )

#         teacher = (
#             user.teacher_profile
#         )

#         allowed = ExamSubject.objects.filter(
#             uuid=exam_subject.uuid,
#             subject_id=teacher.subject_id,
#             exam_class__student_class__in=teacher.students_classes.all(),
#         ).exists()

#         if not allowed:
#             raise PermissionDenied(
#                 "You cannot create marks for this subject/class."
#             )
        
        
        
from accounts.models import CustomUser
from accounts.models import TeacherProfile
from exams.models import ExamSubject
from rest_framework.exceptions import PermissionDenied
from exams.models import Exam
from exams.permission.message import PermissionMessages



class StudentMarkAuthorizer:

    @classmethod
    def _check_core_exam_status(cls, user: CustomUser, exam: Exam):

        if not exam.is_active:
            raise PermissionDenied(PermissionMessages.EXAM_INACTIVE)
        
        if exam.status == "finished":
            raise PermissionDenied(PermissionMessages.EXAM_FINISHED)
    
    @classmethod
    def _check_ongoing_exam_status(cls, user: CustomUser, exam: Exam):
        if exam.status != "ongoing":
            raise PermissionDenied(PermissionMessages.EXAM_NOT_ONGOING)


    @classmethod
    def authorize_create(cls, *, user: CustomUser, exam_subject: ExamSubject):
        exam = exam_subject.exam_class.exam

        if user.is_superuser:
            return

        cls._check_core_exam_status(user=user, exam=exam)

        if user.role == "admin":
            return

        cls._check_ongoing_exam_status(user=user, exam=exam)

        if user.role != "teacher":
            raise PermissionDenied(PermissionMessages.TEACHER_ONLY)

        if cls._teacher_can_access_exam_subject(teacher= user.teacher_profile , exam_subject=exam_subject):
            return True

        raise PermissionDenied(PermissionMessages.TEACHER_NOT_ASSIGNED)

            
    @classmethod
    def _teacher_can_access_exam_subject(cls, teacher: TeacherProfile, exam_subject: ExamSubject):
        return TeacherAssignment.objects.filter(
            teacher=teacher,
            subject=exam_subject.subject,
            student_class=exam_subject.exam_class.student_class 
        ).exists()



    @classmethod
    def authorize_update(cls, *, user: CustomUser, instance: StudentMark):
        exam = instance.exam_subject.exam_class.exam
        if user.is_superuser:
            return 
        
        cls._check_core_exam_status(user=user, exam=exam)

        if user.role == "admin":
            return True
        
        cls._check_ongoing_exam_status(user=user, exam=exam)

        if user.role != "teacher":
            raise PermissionDenied(PermissionMessages.TEACHER_ONLY)

        if cls._teacher_can_access_exam_subject(teacher= user.teacher_profile , exam_subject=instance.exam_subject):
            return True

        raise PermissionDenied(PermissionMessages.TEACHER_NOT_ASSIGNED)
        
        





