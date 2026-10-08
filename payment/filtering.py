from django_filters import rest_framework as filters

# import models
from payment.models import FeePayment



# create filtering


class StudentAcademicInfoFilter(filters.FilterSet):
    class_level = filters.CharFilter(
        field_name="student_class__student_class_level__name",
        lookup_expr="exact",
        label="Class level",
    )

    class Meta:
        model = FeePayment
        fields = [
            "student",
            "student__user",
            "student_class",
            "class_level",
        ]
