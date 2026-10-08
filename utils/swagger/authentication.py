from drf_spectacular.extensions import OpenApiAuthenticationExtension


class UserAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "auth.authentication.UserAuthentication"
    name = "CookieJWTAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "cookie",
            "name": "access_token",
        }


class CSRFAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "auth.csrf_authentication.CSRFAuthentication"
    name = "CSRFToken"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "X-CSRFToken",
        }