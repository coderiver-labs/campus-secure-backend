from accounts.models import CustomUser, StudentProfile
import stripe
from decimal import Decimal

from decouple import config
from django.urls import reverse
import logging
logger = logging.getLogger("security")

# checkout session


def payment_response(student: StudentProfile, quantity: int, fee: Decimal):
    session = create_session(student=student, quantity=quantity, fee=fee)
    return session.url


def create_session(student: StudentProfile, quantity: int, fee: Decimal ):
    unit_amount = int((fee) * 100)

    success_url = f"{config('APP_BASE_URL')}{reverse('payment:success')}"
    cancel_url = f"{config('APP_BASE_URL')}{reverse('payment:cancel')}"


    session = stripe.checkout.Session.create(
        mode="payment",
        customer_email=student.user.email,

        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "School Fee",
                    },
                    "unit_amount": unit_amount,
                },
                "quantity": quantity,
            }
        ],

        success_url=success_url,
        cancel_url=cancel_url,
        
        metadata={
            "student_uuid": str(student.uuid),
            "quantity": str(quantity),
        },
    )
    return session
