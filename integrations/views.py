import hashlib
import hmac
import json

from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView

from .services import SentryWebhookService

from rest_framework.permissions import AllowAny
from decouple import config

# docs
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes


# Sentry Webhook

@extend_schema(
    tags=["Integrations"],
    summary="Handle Sentry Error Webhook",
    description=(
        "Receive error event notifications from Sentry through a webhook. "
        "The webhook validates the Sentry authorization header and processes "
        "only newly created error events. Relevant error information such as "
        "level, project, environment, transaction, and event ID is extracted "
        "and forwarded to the configured Telegram notification service."
    ),
    request=OpenApiTypes.OBJECT,
    responses={
        200: OpenApiResponse(
            description="Sentry error event received and processed successfully."
        ),
        400: OpenApiResponse(
            description=(
                "Invalid or missing authorization, or the request contains "
                "invalid JSON data."
            )
        ),
    },
)
class SentryWebhookView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        body = request.body
        authorization = request.headers.get("Authorization")

        if not authorization:
            return HttpResponse("Missing authorization", status=status.HTTP_400_BAD_REQUEST,)

        expected = f"{config("SENTRY_CLIENT_SECRET")}"
        if not hmac.compare_digest(authorization, expected):
            return HttpResponse("Invalid authorization", status=status.HTTP_400_BAD_REQUEST)
            
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=status.HTTP_400_BAD_REQUEST,)

        SentryWebhookService.handle(payload, request)
        return HttpResponse("OK", status=status.HTTP_200_OK,)
    