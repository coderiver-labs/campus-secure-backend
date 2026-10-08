import time

from django.db import connection

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.public_base_APIView import PublicGenericAPIView
from rest_framework.exceptions import ValidationError

from drf_spectacular.utils import extend_schema, OpenApiResponse


TEST_TAG = ["Test And Error"]



# Create errors






# Status 500 Error 
@extend_schema(
    summary="Trigger division error",
    description="Intentionally triggers a ZeroDivisionError for error monitoring tests.",
    tags=TEST_TAG,
)
class DivisionErrorView(PublicGenericAPIView):
    def get(self, request):
        result = 1 / 0
        return Response({"result": result})
    




# Celery Error

from celery_task.task import celery_error_task, celery_success_task
@extend_schema(
    tags=TEST_TAG,
    summary="Trigger Celery Error Task",
    description=(
        "Trigger a Celery task that intentionally raises an error. "
        "This endpoint is provided for testing Celery error handling "
        "and monitoring behavior."
    ),
    responses={
        200: OpenApiResponse(
            description="Celery error task was successfully queued."
        ),
    },
)
class CeleryDivisionErrorView(PublicGenericAPIView):
    def get(self, request):
        celery_error_task.delay()
        return Response({"Message": "Celery Error Task Called, Check Celery Console"})



@extend_schema(
    tags=TEST_TAG,
    summary="Trigger Celery Success Task",
    description=(
        "Trigger a Celery task that completes successfully. "
        "This endpoint is provided for testing Celery task execution "
        "and successful task monitoring."
    ),
    responses={
        200: OpenApiResponse(
            description="Celery success task was successfully queued."
        ),
    },
)
class CelerySuccessView(PublicGenericAPIView):
    def get(self, request):
        celery_success_task.delay()
        return Response({"Message": "Celery Success Task Called, Check Celery Console"})
    



# DB Error
@extend_schema(
    summary="Trigger database error",
    description="Intentionally executes an invalid SQL query to trigger a database error.",
    tags=TEST_TAG,
)
class DatabaseErrorView(APIView):

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM non_existent_table")
        return Response({"message": "Done"})
    



@extend_schema(
    summary="Simulate slow database query",
    description="Executes a PostgreSQL query with an intentional 3 second delay.",
    tags=TEST_TAG,
)
class SlowDatabaseQueryView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_sleep(3)")
        return Response({"message": "Database query completed after 3 seconds."}, status=status.HTTP_200_OK, )
    

"""_________delay apis___________"""

@extend_schema(
    summary="Simulate 2 second delay",
    description="Delays the response by approximately 2 seconds for performance and tracing tests.",
    tags=TEST_TAG,
)
class Delay2SecondsView(APIView):
    def get(self, request):
        time.sleep(2)
        return Response({"message": "API response after 2 seconds."}, status=status.HTTP_200_OK, )
    

@extend_schema(
    summary="Simulate 5 second delay",
    description="Delays the response by approximately 5 seconds for performance and tracing tests.",
    tags=TEST_TAG,
)
class Delay5SecondsView(APIView):
    def get(self, request):
        time.sleep(5)
        return Response({"message": "API response after 5 seconds."}, status=status.HTTP_200_OK, )
    


@extend_schema(
    summary="Simulate 10 second delay",
    description="Delays the response by approximately 10 seconds for performance and tracing tests.",
    tags=TEST_TAG,
)
class Delay10SecondsView(APIView):
    def get(self, request):
        time.sleep(10)
        return Response({"message": "API response after 10 seconds."}, status=status.HTTP_200_OK, )
    




### CPU HeavyLoad
@extend_schema(
    summary="Simulate CPU intensive request",
    description="Performs a CPU-intensive calculation for performance monitoring tests.",
    tags=["Test And Error"],
)
class CPUHeavyView(APIView):
    def get(self, request):
        total = 0
        for number in range(5_000_000):
            total += number ** 2
        return Response({"message": "CPU intensive task completed.","result": total,}, status=status.HTTP_200_OK,)



