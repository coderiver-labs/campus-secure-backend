from django.db import models

# import modes 
from accounts.base_model import BaseModel
from accounts.models import StudentProfile
from school.models import StudentClass




class FeePayment(BaseModel):
    CALENDAR_CHOICE=[
        (1, "January"), (2, "February"),
        (3, "March"), (4, "April"),
        (5, "May"), (6, "June"),
        (7, "July"), (8, "August"),
        (9, "September"), (10, "October"),
        (11, "November"), (12, "December"),
    ]


    PAYMENT_METHOD_CHOICES = [
        ("stripe", "Stripe"),
        ("cash", "Cash"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="fee_payments",)
    student_class = models.ForeignKey(StudentClass, on_delete=models.PROTECT, related_name="fee_payments", )

    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField(choices=CALENDAR_CHOICE)

    amount = models.DecimalField(max_digits=10, decimal_places=2,)

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES,)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending",)
    
    paid_at = models.DateTimeField(null=True, blank=True, )

    stripe_session_id = models.CharField(max_length=255, null=True, blank=True,)
    stripe_payment_intent = models.CharField(max_length=255, null=True, blank=True,)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "student_class",
                    "year",
                    "month",
                ],
                name="unique_student_class_fee_month",
            )
        ]