from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.middleware.csrf import CsrfViewMiddleware

# import logger 



# create your csrf authentication hare

class CSRFAuthentication(BasicAuthentication):
    """
    Runs Django's CSRF validation for incoming request.
    Returns None since this class doesn't authenticate users — only validates CSRF.
    """
    def authenticate(self, request):
        csrf_middleware = CsrfViewMiddleware(lambda req:None)
        reason = csrf_middleware.process_view(request=request, callback=None, callback_args=(), callback_kwargs={})
        if reason:
            raise AuthenticationFailed("CSRF validation failed")
        return None