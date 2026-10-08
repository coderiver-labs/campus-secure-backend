from django.utils.decorators import method_decorator

# import rest
from auth.cookies import CookieHandler



# create Mixin hare

class CSRFCookieMixin:
    """
    Automatically attach CSRF token to response cookie.
    """
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        cookie = CookieHandler(request=request, user=getattr(request, "user", None), response=response)
        cookie.set_csrf_token()
        return cookie.get_response()


    

