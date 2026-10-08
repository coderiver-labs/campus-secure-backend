import time
import logging
# from django.http import HttpResponse, HttpRequest, request
from rest_framework.request import HttpRequest
from rest_framework.response import Response

# prometheus
from prometheus_client import Histogram, Counter

logger = logging.getLogger("performance")


# create middleware to log request performance



REQUEST_LATENCY = Histogram(
    "drf_request_duration_seconds",
    "Request latency",
    ["method", "endpoint", "status"]
)

REQUEST_COUNT = Counter(
    "drf_requests_total",
    "Total requests",
    ["method", "endpoint", "status"]
)




class RequestPerformanceMiddleware:
    """
    Logs request execution time.
    """

    SLOW_REQUEST_THRESHOLD_MS = 1000  # 1 second

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> Response:
        start_time = time.perf_counter()

        response = self.get_response(request)

        duration = time.perf_counter() - start_time
        duration_ms = round(duration * 1000, 2)

        endpoint = request.path

        # 👉 metrics (NEW)
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).observe(duration)

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()

        # 👉 existing logs (KEEP)
        log_data = {
            "action": "request_complete",
            "method": request.method,
            "path": endpoint,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        }

        if duration_ms > self.SLOW_REQUEST_THRESHOLD_MS:
            logger.warning("Slow request detected", extra=log_data)
        else:
            logger.info("Request completed", extra=log_data)

        return response
