from accounts.models import StudentProfile
from django_filters import rest_framework as filters



# import Filter



class StudentAcademicInfoFilter(filters.FilterSet):
    student_class = filters.CharFilter(
        field_name="academic_info__student_class",
        lookup_expr="exact",
        label="Student Class",
    )
    class_level = filters.CharFilter(
        field_name="academic_info__student_class__student_class_level__name",
        lookup_expr="exact",
        label="Class level",
    )

    class Meta:
        model = StudentProfile
        fields = ["student_class", "class_level",]



