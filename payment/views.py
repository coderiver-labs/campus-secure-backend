from django.conf import settings
from payment.service.stripe_webhook import handle_checkout_session

# import DRF
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer

# import models
from school.models import ClassLevel

# import serializer
from payment.serializers import SchoolFeeSerializer, StudentFeeCheckoutSerializer

# import utils
from utils.public_base_APIView import PublicGenericAPIView

# import services
from payment.service.calculation import student_fee
from payment.service.stripe_session import payment_response


# import stripe
import stripe

# import python
from typing import cast

# docs
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse



# create your views

@extend_schema(
    tags=["Payment Callback"],
    summary="Payment Success",
    description=(
        "Handle the successful payment callback and return a confirmation "
        "message after a successful payment flow."
    ),
)
class SuccessPaymentAPIView(PublicGenericAPIView):
    def get(self, request):
        return Response({"message": "payment success"}, status=status.HTTP_200_OK)

@extend_schema(
    tags=["Payment Callback"],
    summary="Payment Cancelled",
    description=(
        "Handle the cancelled payment callback and return a confirmation "
        "message when the payment process is cancelled."
    ),
)
class CancelPaymentAPIView(PublicGenericAPIView):
    def get(self, request):
        return Response({"message": "payment cancel"})
    
    
    
from payment.service.calculation import remaining_month

@extend_schema_view(
    get=extend_schema(
        tags=["Payment Checkout"],
        summary="List School Fee Plans",
        description=(
            "Retrieve the available school classes and their applicable "
            "school fee information. This endpoint is publicly accessible "
            "and can be used to view the available fee plans before starting "
            "a payment."
        ),
    ),
    post=extend_schema(
        tags=["Payment Checkout"],
        summary="Create Student Fee Checkout",
        description=(
            "Create a payment checkout session for a student. "
            "Provide the student's email and student class to calculate "
            "the applicable school fee and generate a Stripe checkout URL. "
            "If the student's school fee for the current year is already "
            "complete, no checkout session will be created."
        ),
        request=StudentFeeCheckoutSerializer,
        responses={
            200: OpenApiResponse(
                description=(
                    "Returns the student's name and the generated "
                    "payment checkout URL."
                ),
            ),
        },
    ),
)
class SchoolMonthlyPlanView(PublicGenericAPIView):

    def get_serializer_class(self):
        if self.request.method == "POST":
            return StudentFeeCheckoutSerializer
        return SchoolFeeSerializer

    def get_queryset(self):
        return ClassLevel.objects.all()

    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({"data": serializer.data})


    def post(self, request):
        serializer = cast(Serializer, self.get_serializer(data=request.data))
        serializer.is_valid(raise_exception=True)
        remaining_months = serializer.validated_data["remaining_months"]
        if remaining_months == 0:
            return Response({"message": "Student's school fee is complete for this year."}, status=status.HTTP_200_OK)

        quantity = serializer.validated_data["quantity"]
        student = serializer.validated_data["student"]
        fee = student_fee(student=student)
        url = payment_response(student=student, quantity=quantity, fee=fee)
        return Response({"student": student.user.get_full_name(), "url": url}, status=status.HTTP_200_OK)


from utils.serializers import DummySerializer
# This api ony for stripe

@extend_schema(
    tags=["Stripe Webhook"],
    summary="Handle Stripe Webhook",
    description=(
        "Receive and process Stripe webhook events for payment processing. "
        "The request is verified using the Stripe webhook signature before "
        "processing the event. When a checkout session is completed, the "
        "corresponding payment session is processed and the payment record "
        "is handled by the backend."
    ),
    request=None,
    responses={
        200: OpenApiResponse(
            description="Stripe webhook processed successfully."
        ),
        400: OpenApiResponse(
            description="Invalid payload or invalid Stripe signature."
        ),
    },
)
class StripeWebhookView(PublicGenericAPIView):
    authentication_classes = []
    serializer_class = DummySerializer

    def post(self, request: HttpRequest):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret, )
        except ValueError:
            return Response({"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST, )
        except stripe.error.SignatureVerificationError:
            return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST, )

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            handle_checkout_session(session=session, request=request)
        return Response({"status": "success"}, status=status.HTTP_200_OK)
    




# Admin panel 
from payment.base_views import BaseFeePaymentView
from django.db import transaction
from audit.services import AuditService
from payment.permissions.policy import FeePaymentManageViewPolicy


@extend_schema_view(
    list=extend_schema(
        tags=["Payments"],
        summary="List Fee Payments",
        description=(
            "Retrieve a list of student fee payments with support for "
            "filtering, searching, and ordering."
        ),
    ),
    create=extend_schema(
        tags=["Payments"],
        summary="Create Fee Payment",
        description=(
            "Create a new school fee payment record for a student."
        ),
    ),
    retrieve=extend_schema(
        tags=["Payments"],
        summary="Retrieve Fee Payment",
        description=(
            "Retrieve details of a specific student fee payment."
        ),
    ),
    update=extend_schema(
        tags=["Payments"],
        summary="Update Fee Payment",
        description=(
            "Update an existing student fee payment record."
        ),
    ),
    partial_update=extend_schema(
        tags=["Payments"],
        summary="Partially Update Fee Payment",
        description=(
            "Partially update an existing student fee payment record."
        ),
    ),
)
class FeePaymentManageView(BaseFeePaymentView):
    permission_classes = [FeePaymentManageViewPolicy]

    def get_queryset(self):
        queryset = super().get_queryset()
        policy_class = self.permission_classes[0]
        return policy_class.scope_queryset(request=self.request, qs=queryset)
    

    def perform_create(self, serializer: Serializer):
        with transaction.atomic():
            instance = serializer.save()
            AuditService.create_log(
                actor=self.request.user,
                instance=instance,
                request=self.request,
                description="School FeePayment Created"
            )
            
    
    def perform_update(self, serializer: Serializer):
        with transaction.atomic():
            instance = self.get_object()
            AuditService.update_log(
                actor=self.request.user,
                instance=instance,
                validated_data=serializer.validated_data,
                request=self.request,
                description="School FeePayment Updated"
            )
            serializer.save()
