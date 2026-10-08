import uuid
from rest_framework.request import Request

class RequestIDMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid.uuid4())
        return self.get_response(request)