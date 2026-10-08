from __future__ import annotations
from django.apps import apps
import json
from calendar import monthrange

from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.utils import timezone


# create dashboard

def _monthly_buckets(months: int = 6):
    """
    Return:
        labels      -> ["Apr", "May", ...]
        month_starts -> datetime objects for the first day of each month

    Oldest month first.
    """
    now = timezone.now()

    buckets = []

    year = now.year
    month = now.month

    for _ in range(months - 1):
        month -= 1

        if month == 0:
            month = 12
            year -= 1

    for _ in range(months):
        buckets.append(
            timezone.datetime(
                year,
                month,
                1,
                tzinfo=now.tzinfo,
            )
        )

        month += 1

        if month == 13:
            month = 1
            year += 1

    labels = [date.strftime("%b") for date in buckets]

    return labels, buckets


def dashboard_callback(request, context):
    User = get_user_model()

    # -----------------------------------------------------------
    # Actual models
    # -----------------------------------------------------------

    StudentProfile = apps.get_model("accounts", "StudentProfile")
    TeacherProfile = apps.get_model("accounts", "TeacherProfile")
    AdminProfile = apps.get_model("accounts", "AdminProfile")
    StaffProfile = apps.get_model("accounts", "StaffProfile")
    StudentClass = apps.get_model("school", "StudentClass")
    Exam = apps.get_model("exams", "Exam")
    FeePayment = apps.get_model("payment", "FeePayment")

    # -----------------------------------------------------------
    # ROW 1
    # KPI cards
    # -----------------------------------------------------------

    total_users = User.objects.count()

    # StudentProfile has OneToOne relation with CustomUser.
    total_students = StudentProfile.objects.count()

    # StaffProfile also has OneToOne relation with CustomUser.
    total_staff = StaffProfile.objects.count()

    
    total_teacher = TeacherProfile.objects.count()
    total_admin = AdminProfile.objects.count()

    # Your StudentClass is the actual class/section entity.
    total_classes = StudentClass.objects.count()

    # -----------------------------------------------------------
    # Revenue
    # -----------------------------------------------------------
    #
    # IMPORTANT:
    # Replace "success" with your actual successful payment status
    # if your FeePayment model uses another choice.
    #

    total_revenue = (
        FeePayment.objects
        .filter(status="success")
        .aggregate(total=Sum("amount"))["total"]
        or 0
    )

    pending_payments = FeePayment.objects.filter(
        status="pending"
    ).count()

    # -----------------------------------------------------------
    # ROW 2
    # Enrollment trend
    # -----------------------------------------------------------

    labels, month_starts = _monthly_buckets(6)

    enrollment_data = []

    for index, start in enumerate(month_starts):

        if index + 1 < len(month_starts):
            end = month_starts[index + 1]
        else:
            end = timezone.now()

        count = StudentProfile.objects.filter(
            created_at__gte=start,
            created_at__lt=end,
        ).count()

        enrollment_data.append(count)

    # -----------------------------------------------------------
    # Role distribution
    # -----------------------------------------------------------

    role_distribution = {
        "labels": [
            "Students",
            "Staff",
            "Teachers",
            "Admins",
        ],
        "data": [
            User.objects.filter(role="student").count(),
            User.objects.filter(role="staff").count(),
            User.objects.filter(role="teacher").count(),
            User.objects.filter(
                role="admin"
            ).count(),
        ],
    }

    # -----------------------------------------------------------
    # ROW 3
    # Payment breakdown
    # -----------------------------------------------------------

    payments_breakdown = {
        "labels": [
            "Successful",
            "Pending",
            "Failed",
        ],
        "data": [
            FeePayment.objects.filter(
                status="success"
            ).count(),

            FeePayment.objects.filter(
                status="pending"
            ).count(),

            FeePayment.objects.filter(
                status="failed"
            ).count(),
        ],
    }

    # -----------------------------------------------------------
    # Upcoming exams
    # -----------------------------------------------------------

    upcoming_exams = []

    if Exam is not None:

        qs = (
            Exam.objects
            .filter(start_date__gte=timezone.now())
            .order_by("start_date")[:5]
        )

        for exam in qs:
            upcoming_exams.append(
                {
                    "title": getattr(
                        exam,
                        "name",
                        str(exam),
                    ),
                    "date": getattr(
                        exam,
                        "start_date",
                        None,
                    ),
                }
            )

    # -----------------------------------------------------------
    # ROW 4
    # Recent registrations
    # -----------------------------------------------------------

    recent_registrations = []

    qs = User.objects.order_by("-created_at")[:5]

    for user in qs:

        if user.is_superuser:
            role = "superuser"
        else:
            role = user.role

        recent_registrations.append(
            {
                "name": user.get_full_name(),
                "email": user.email,
                "role": role,
                "date": user.created_at,
            }
        )

    # -----------------------------------------------------------
    # Recent payments
    # -----------------------------------------------------------

    recent_payments = []

    qs = (
        FeePayment.objects
        .select_related()
        .order_by("-created_at")[:5]
    )

    for payment in qs:

        student = getattr(
            payment,
            "student",
            getattr(
                payment,
                "user",
                "",
            ),
        )

        recent_payments.append(
            {
                "student": str(student),
                "amount": payment.amount,
                "status": payment.status,
                "date": payment.created_at,
            }
        )

    # Context

    context.update(
        {
            # KPI
            "total_users": total_users,
            "total_students": total_students,
            "total_teacher": total_teacher,
            "total_admin": total_admin,
            "total_staff": total_staff,
            "active_classes": total_classes,
            "total_revenue": total_revenue,
            "pending_payments": pending_payments,

            # Enrollment chart
            "enrollment_labels": json.dumps(labels),
            "enrollment_data": json.dumps(enrollment_data),

            # Role chart
            "role_distribution_labels": json.dumps(
                role_distribution["labels"]
            ),
            "role_distribution_data": json.dumps(
                role_distribution["data"]
            ),

            # Payment chart
            "payments_labels": json.dumps(
                payments_breakdown["labels"]
            ),
            "payments_data": json.dumps(
                payments_breakdown["data"]
            ),

            # Tables
            "upcoming_exams": upcoming_exams,
            "recent_registrations": recent_registrations,
            "recent_payments": recent_payments,
        }
    )

    return context

