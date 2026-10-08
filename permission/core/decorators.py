from functools import wraps
# DRF
from rest_framework.request import HttpRequest
# import models
from accounts.models import CustomUser



# create decorators

def superuser_bypass(method):
    @wraps(method)
    def wrapper(self, request:HttpRequest, *args, **kwargs):
        user = request.user

        if getattr(user, "is_superuser", False):
            return True
        return method(self, request, *args, **kwargs)
    return wrapper
