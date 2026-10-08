
from exams.models import ExamSubject, StudentMark

# import Filter
from django_filters import rest_framework as filters


class ExamSubjectFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(
        field_name="exam_class__exam__is_active",
        lookup_expr="exact",
        label="Exam",
    )
    status = filters.CharFilter(
        field_name="exam_class__exam__status",
        lookup_expr="exact",
        label="Status",
    )
    exam_name = filters.CharFilter(
        field_name="exam_class__exam__name",
        lookup_expr="iexact",
        label="Exam Name",
    )
    subject_name = filters.CharFilter(
        field_name="subject__name",
        lookup_expr="exact",
        label="Subject Name",
    )
    class_level = filters.CharFilter(
        field_name="student_class__student_class_level__name",
        lookup_expr="exact",
        label="Class level",
    )
    class Meta:
        model = ExamSubject
        fields = ["is_active", "status", "exam_name", "subject_name", "class_level", "full_mark", "pass_mark"]


class StudentMarkFilter(filters.FilterSet):
    exam_class = filters.UUIDFilter(
        field_name="exam_subject__exam_class__uuid",
        lookup_expr="exact",
        label="Exam Class",
    )
    is_active = filters.BooleanFilter(
        field_name="exam_subject__exam_class__exam__is_active",
        lookup_expr="exact",
        label="Is Active Exam",
    )


    exam_name = filters.CharFilter(
        field_name="exam_subject__exam_class__exam__name",
        lookup_expr="iexact, icontains ",
        label="Exam Name",
    )
    student_class = filters.UUIDFilter(
        field_name="exam_subject__exam_class__student_class",
        lookup_expr="exact",
        label="Student Class",
    )
    subject = filters.UUIDFilter(
        field_name="exam_subject__subject",
        lookup_expr="exact",
        label="Exam Subject",
    )

    subject_name = filters.CharFilter(
        field_name="exam_subject__subject__name",
        lookup_expr="iexact",
        label="Exam Subject Name",
    )

    first_name = filters.UUIDFilter(
        field_name="student__user__first_name",
        lookup_expr="iexact",
        label="User first Name",
    )


    class Meta:
        model = StudentMark
        fields = [
            "exam_class",
            "is_active",
            "exam_name",
            "student_class",
            "subject",
            "subject_name",
            "first_name",
            "student",
            "marks_obtained",
            "is_absent",
        ]
