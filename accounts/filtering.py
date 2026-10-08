from accounts.models import StudentAcademicInfo

# import Filter
from django_filters import rest_framework as filters


class StudentAcademicInfoFilter(filters.FilterSet):
    class_level = filters.CharFilter(
        field_name="student_class__student_class_level__name",
        lookup_expr="exact",
        label="Class level",
    )

    class Meta:
        model = StudentAcademicInfo
        fields = [
            "start_year",
            "end_year",
            "class_level",
            "student_class",
            "roll_number",
            "admission_date",
            "previous_school"
        ]


from accounts.models import StudentParentsInfo
class StudentParentsInfoViewFilter(filters.FilterSet):
    class Meta:
        model = StudentParentsInfo
        fields = {
            "father_name": ["iexact"],
            "mother_name": ["iexact"],
            "father_phone": ["exact"],
            "mother_phone": ["exact"]
        }