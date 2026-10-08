from django.utils import timezone

# DRF
from rest_framework.serializers import Serializer

# import models
from accounts.models import StudentProfile
from payment.models import FeePayment


# create calculation





from django.db.models import Q
from django.utils import timezone


def has_open_payment(student):
    return FeePayment.objects.filter(
        student=student,
        student_class=student.academic_info.student_class,
        year=timezone.localdate().year,
    ).filter(Q(status="failed") | Q(status="pending")).exists()


def student_fee(student) -> int:
    student_monthly_fee = student.academic_info.student_class.student_class_level.monthly_fee
    return student_monthly_fee



def remaining_month(student: StudentProfile):
    paid_months = FeePayment.objects.filter(
        student=student,
        student_class=student.academic_info.student_class,
        year=timezone.localdate().year,
        status="success",
    ).values_list("month", flat=True)

    return 12 - len(set(paid_months))

