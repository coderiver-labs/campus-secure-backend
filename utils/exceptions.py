from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.request import Request, HttpRequest
from rest_framework import status

# import logger and sentry
import sentry_sdk
import logging
logger = logging.getLogger("error")



# # create exception hare


# def custom_exception_handler(exc: Exception, context: dict):
#     response = exception_handler(exc, context)

#     # Expected errors (ValidationError, PermissionDenied, etc.)
#     if response is not None:
#         return Response(
#             {
#                 "success": False,
#                 "status_code": response.status_code,
#                 "errors": response.data,
#             },
#             status=response.status_code,
#         )

#     # Unexpected error → capture to Sentry
#     request: HttpRequest = context.get("request")

#     with sentry_sdk.push_scope() as scope:
#         if request:
#             # Attach user (if authenticated)
#             if hasattr(request, "user") and request.user.is_authenticated:
#                 scope.set_user({
#                     "id": str(request.user.uuid)
#                 })

#             # Attach request_id if exists
#             scope.set_extra(
#                 "request_id",
#                 getattr(request, "request_id", None)
#             )

#             # Optional: add path + method
#             scope.set_extra("path", request.path)
#             scope.set_extra("method", request.method)

#         # Finally capture the exception
#         sentry_sdk.capture_exception(exc)

#     # Log structured error locally
#     logger.error(
#         "Unhandled server error",
#         extra={
#             "action": "unhandled_exception",
#             "error_type": exc.__class__.__name__,
#         },
#         exc_info=True,
#     )

#     # Return safe generic response
#     return Response(
#         {
#             "success": False,
#             "status_code": 500,
#             "errors": {"detail": "Something went wrong on server."},
#         },
#         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#     )





from django.http import HttpRequest
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

import sentry_sdk

from prometheus_client import Counter


unhandled_exceptions = Counter(
    "django_unhandled_exceptions_total",
    "Total number of unhandled application exceptions.",
    ["view", "exception_type"],
)

def custom_exception_handler(exc: Exception, context: dict):

    response = exception_handler(exc, context)

    # Expected errors
    if response is not None:
        return Response(
            {
                "success": False,
                "status_code": response.status_code,
                "errors": response.data,
            },
            status=response.status_code,
        )

    # Unexpected error → capture to Sentry
    request: HttpRequest = context.get("request")

    with sentry_sdk.push_scope() as scope:

        if request:
            if hasattr(request, "user") and request.user.is_authenticated:
                scope.set_user({
                    "id": str(request.user.uuid),
                })

            scope.set_extra(
                "request_id",
                getattr(request, "request_id", None),
            )

            scope.set_extra("path", request.path)
            scope.set_extra("method", request.method)

        sentry_sdk.capture_exception(exc)

    # Structured logging
    logger.error(
        "Unhandled server error",
        extra={
            "action": "unhandled_exception",
            "error_type": exc.__class__.__name__,
        },
        exc_info=True,
    )

    # Prometheus
    view = context.get("view")
    view_name = (
        view.__class__.__name__
        if view
        else "unknown"
    )

    unhandled_exceptions.labels(
        view=view_name,
        exception_type=exc.__class__.__name__,
    ).inc()

    # Safe generic response
    return Response(
        {
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "errors": {
                "detail": "Something went wrong on server.",
            },
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )