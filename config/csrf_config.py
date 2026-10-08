from decouple import config, Csv

"""CSRF Configure"""
CSRF_COOKIE_AGE = int(604800) # 7d

CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_HTTPONLY = False   # JavaScript থেকে access করতে চাইলে False
CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"
CSRF_USE_SESSIONS = False
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv()) # For Django Admin Panel

