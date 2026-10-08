from functools import wraps

# Only Superuser allow
def default_allow_superuser(method):
    @wraps(method)
    def _impl(self, request, view, action):
        if getattr(request.user, "is_superuser", False):
            return True
        return method(self, request, view, action)
    return _impl

# Superuser and Admin allow 
def default_allow_admin_and_superuser(method):
    @wraps(method)
    def _impl(self, request, view, action):
        user = getattr(request, "user", None)
        if getattr(user, "is_superuser", False) or getattr(user, "role", None) == "admin":
            return True
        return method(self, request, view, action)
    return _impl