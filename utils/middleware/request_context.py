import uuid
import logging
from threading import local
_request_storage = local()


# Get the current request from thread-local storage

def get_current_request():
    return getattr(_request_storage, "request", None)

class RequestContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid.uuid4())
        _request_storage.request = request
        response = self.get_response(request)
        return response
    
    