REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "auth.authentication.CSRFAuthentication", # csrf authentication
        "auth.authentication.UserAuthentication", # cookie base authentication
    ),
    
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'login': '5/min',          # login a 1mon a max 5 bar try korte parbe 
        "api": "100/min",
    },

    # custom exception
    "EXCEPTION_HANDLER": "utils.exceptions.custom_exception_handler",
    
    # for API AutoDocs  
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    
    # custom renderer
    "DEFAULT_RENDERER_CLASSES": (
        "utils.global_renders.GlobalJSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
    ),
    
    # pagination
    
    "DEFAULT_PAGINATION_CLASS": "utils.pagination.CustomPageNumberPagination",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],

    # api version
    # "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    # "DEFAULT_VERSION": "v1",
    # "ALLOWED_VERSIONS": ["v1", "v2"],

}

