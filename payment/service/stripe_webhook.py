from django.db import transaction
from django.utils import timezone

# import models
from accounts.models import StudentProfile
from payment.models import FeePayment

# import stripe
import stripe

# audit log
from audit.services import AuditService



# create webhook services

def get_student(student_uuid):
    try:
        return StudentProfile.objects.select_related(
            "user",
            "academic_info",
            "academic_info__student_class",
            "academic_info__student_class__student_class_level",
        ).get(uuid=student_uuid)

    except StudentProfile.DoesNotExist:
        raise ValueError("Student not found")
    
    

from rest_framework.request import Request
from celery_task.task import celery_send_receipt_email
import logging
logger = logging.getLogger(__name__)
def handle_checkout_session(session: stripe.checkout.Session, request: Request):
    metadata = session.get("metadata", {})

    student_uuid = metadata.get("student_uuid")
    quantity = int(metadata.get("quantity", 0))

    student = get_student(student_uuid=student_uuid)

    try:
        student = get_student(student_uuid=student_uuid)
    except Exception as e:
        logger.error(f"Student not found for UUID {student_uuid}: {str(e)}")
        return
    

    current_class = student.academic_info.student_class
    current_year = timezone.localdate().year

    paid_months = set(
        FeePayment.objects.filter(
            student=student,
            student_class=current_class,
            year=current_year,
            status="success",
        ).values_list("month", flat=True)
    )

    unpaid_months = [
        month
        for month in range(1, 13)
        if month not in paid_months
    ]

    selected_months = unpaid_months[:quantity]
    monthly_fee = current_class.student_class_level.monthly_fee

    created_payment_uuids = []

    with transaction.atomic():
        for month in selected_months:
            instance = FeePayment.objects.create(
                student=student,
                student_class=current_class,
                year=current_year,
                month=month,
                amount=monthly_fee,
                payment_method="stripe",
                status="success",
                paid_at=timezone.now(),
                stripe_session_id=session["id"],
                stripe_payment_intent=session.get("payment_intent"),
            )

            created_payment_uuids.append(str(instance.uuid))

            AuditService.create_log(
                actor=None,
                instance=instance,
                request=request,
                description="Stripe Webhook Payment"
            )
        transaction.on_commit(
            lambda: celery_send_receipt_email.delay(
                student_uuid=str(student.uuid),
                payment_uuids=created_payment_uuids,
            )
        )